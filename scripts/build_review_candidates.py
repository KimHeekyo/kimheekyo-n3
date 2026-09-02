#!/usr/bin/env python3
"""Build a review queue by matching imported words against a JMdict SQLite pack.

This does not publish data.  It creates evidence for human review: canonical
reading/POS, dictionary senses, and examples attached to those senses.
"""

import argparse
import json
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORDS_JS = ROOT / "data" / "words.js"
OPENJLPT = ROOT / "data" / "openjlpt-n3.json"
OUTPUT = ROOT / "data" / "review-candidates.json"
KANJI = re.compile(r"[\u3400-\u9fff々]")
KATAKANA = re.compile(r"[ァ-ヺー]")

# Orthographic variants which are folded into another JMdict entry.  The
# imported spelling is retained unless the source form itself is malformed.
JM_DICT_ALIASES = {
    "明ける": 209090, "現す": 214955, "或": 245891,
    "降ろす": 246155, "換える": 246175, "曇": 246430,
    "支払": 246638, "唯": 241399, "年寄": 247060,
    "昇る": 223509, "二十": 247261, "人込み": 224959,
    "独り": 244861, "濠": 239786, "祭": 247589,
    "向かい": 247651, "よると": 191669,
    "コンピューター": 195534, "ソファー": 197523,
    "いたずら": 204232, "いち": 219221, "あんまり": 245718,
    "けち": 304195, "務め": 212768,
}

ENGLISH_STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "but", "by", "e.g", "for",
    "from", "in", "of", "on", "or", "the", "to", "with",
}


def has_safe_occurrence(sentence, word):
    start = 0
    while True:
        index = sentence.find(word, start)
        if index < 0:
            return False
        before = sentence[index - 1] if index else ""
        after_index = index + len(word)
        after = sentence[after_index] if after_index < len(sentence) else ""
        script = KANJI if KANJI.search(word) else KATAKANA if KATAKANA.search(word) else None
        if script is None or not (script.fullmatch(before) or script.fullmatch(after)):
            return True
        start = index + 1


def load_words():
    text = WORDS_JS.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def load_source_meanings():
    source = json.loads(OPENJLPT.read_text(encoding="utf-8"))
    return {item["word"]: item.get("meanings", []) for item in source}


def english_tokens(values):
    return {
        token
        for value in values
        for token in re.findall(r"[a-z]+", value.lower())
        if token not in ENGLISH_STOPWORDS and len(token) > 1
    }


def choose_entry(db, word, kana, source_meanings):
    if word in JM_DICT_ALIASES:
        return db.execute(
            "SELECT id, headword, romanized, pos, source, priority, freq_rank "
            "FROM entries WHERE id=?", (JM_DICT_ALIASES[word],)
        ).fetchone()
    select = """
        SELECT id, headword, romanized, pos, source, priority, freq_rank
        FROM entries
        WHERE source = 'jmdict' AND {column} = ?
        ORDER BY CASE WHEN romanized = ? THEN 0 ELSE 1 END,
                 priority DESC,
                 CASE WHEN freq_rank IS NULL THEN 1 ELSE 0 END,
                 freq_rank, id
    """
    rows = db.execute(select.format(column="headword"), (word, kana)).fetchall()
    if not rows:
        rows = db.execute(select.format(column="romanized"), (word, kana)).fetchall()
    if len(rows) < 2 or not source_meanings:
        return rows[0] if rows else None

    wanted = english_tokens(source_meanings)
    ranked = []
    for row in rows:
        definitions = [
            sense[0] for sense in db.execute(
                "SELECT definition FROM senses WHERE entry_id=? AND def_lang='en'",
                (row[0],),
            )
        ]
        overlap = len(wanted & english_tokens(definitions))
        ranked.append((overlap, row[1] == word, row))
    return max(ranked, key=lambda item: (item[0], item[1]))[2]


def senses_for(db, entry_id, language):
    return [
        {"id": row[0], "definition": row[1], "tags": row[2]}
        for row in db.execute(
            "SELECT id, definition, tags FROM senses WHERE entry_id=? AND def_lang=? ORDER BY id",
            (entry_id, language),
        )
    ]


def korean_senses_for_words(db, *headwords):
    terms = [word for word in dict.fromkeys(headwords) if word]
    if not terms:
        return []
    placeholders = ",".join("?" for _ in terms)
    return [
        {"id": row[0], "definition": row[1], "tags": row[2], "source": row[3]}
        for row in db.execute(
            f"""
            SELECT DISTINCT s.id, s.definition, s.tags, e.source
            FROM entries e JOIN senses s ON s.entry_id=e.id
            WHERE e.headword IN ({placeholders}) AND s.def_lang='ko'
            ORDER BY CASE e.source WHEN 'kaikki-kowikt' THEN 0 ELSE 1 END, s.id
            """,
            terms,
        )
    ]


def examples_for(db, sense_ids, word, limit=8):
    if not sense_ids:
        return []
    placeholders = ",".join("?" for _ in sense_ids)
    rows = db.execute(
        f"""
        SELECT source_text, translation, sense_id
        FROM examples
        WHERE sense_id IN ({placeholders}) AND source_lang='ja'
        ORDER BY
          CASE WHEN instr(source_text, ?) > 0 THEN 0 ELSE 1 END,
          length(source_text), id
        LIMIT ?
        """,
        (*sense_ids, word, max(limit * 8, 64)),
    ).fetchall()
    return [
        {"ja": row[0], "en": row[1], "sense_id": row[2]}
        for row in rows
        if row[0] and row[1] and has_safe_occurrence(row[0], word)
    ][:limit]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    db = sqlite3.connect(args.database)
    source_meanings = load_source_meanings()
    result = []
    matched = 0
    korean = 0
    examples = 0

    for imported in load_words():
        original_meanings = source_meanings.get(imported["word"], [])
        entry = choose_entry(db, imported["word"], imported["kana"], original_meanings)
        candidate = {
            "imported": imported,
            "status": "unmatched",
            "dictionary": None,
            "ko_senses": [],
            "en_senses": [],
            "examples": [],
            "source_meanings": original_meanings,
        }
        if entry:
            matched += 1
            entry_id, headword, reading, pos, source, priority, freq_rank = entry
            ko_senses = korean_senses_for_words(db, imported["word"], headword)
            en_senses = senses_for(db, entry_id, "en")
            linked_examples = examples_for(
                db, [sense["id"] for sense in en_senses], imported["word"]
            )
            korean += bool(ko_senses)
            examples += bool(linked_examples)
            candidate.update(
                {
                    "status": "matched",
                    "dictionary": {
                        "entry_id": entry_id,
                        "word": headword,
                        "kana": reading or imported["kana"],
                        "pos": pos,
                        "source": source,
                        "priority": priority,
                        "frequency_rank": freq_rank,
                    },
                    "ko_senses": ko_senses,
                    "en_senses": en_senses,
                    "examples": linked_examples,
                }
            )
        result.append(candidate)

    payload = {
        "schema_version": 1,
        "source": "JMdict via Kotobase ja_core",
        "counts": {
            "total": len(result),
            "matched": matched,
            "with_korean_sense": korean,
            "with_linked_example": examples,
        },
        "entries": result,
    }
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
