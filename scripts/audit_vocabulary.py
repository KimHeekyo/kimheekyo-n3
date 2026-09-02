#!/usr/bin/env python3
"""Validate the offline vocabulary bundle before packaging or deployment."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "words.js"
APP = ROOT / "app.js"
REQUIRED = ("word", "kana", "meaning", "type", "example", "translation")
KANA = re.compile(r"[ぁ-ゖァ-ヺー・\s]+")


def load_words():
    text = SOURCE.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def primary_meaning(word):
    return word["meaning"].split(",", 1)[0].strip()


def main():
    words = load_words()
    errors = []
    app_source = APP.read_text(encoding="utf-8")

    for index, word in enumerate(words):
        for field in REQUIRED:
            if not str(word.get(field, "")).strip():
                errors.append(f"#{index} {word.get('word', '?')}: empty {field}")
        if word.get("kana") and not KANA.fullmatch(word["kana"]):
            errors.append(f"#{index} {word['word']}: invalid kana {word['kana']!r}")
        if ";" in word.get("meaning", "") or "；" in word.get("meaning", ""):
            errors.append(f"#{index} {word['word']}: semicolon in meaning")
        senses = [sense.strip() for sense in word.get("meaning", "").split(",")]
        if len(senses) != len(set(senses)):
            errors.append(f"#{index} {word['word']}: repeated meaning")

    duplicates = [word for word, count in Counter(w["word"] for w in words).items() if count > 1]
    errors.extend(f"duplicate word: {word}" for word in duplicates)

    # The UI needs one correct option and at least three distinct distractors in both directions.
    for direction in ("jp-ko", "ko-jp"):
        values = [primary_meaning(w) if direction == "jp-ko" else w["word"] for w in words]
        unique = set(values)
        if len(unique) < 4:
            errors.append(f"{direction}: fewer than four distinct option values")
        for index, correct in enumerate(values):
            if not correct:
                errors.append(f"#{index} {direction}: empty correct option")

    for index, word in enumerate(words):
        correct_meaning = primary_meaning(word)
        eligible = {
            candidate["word"]
            for candidate in words
            if candidate is not word and primary_meaning(candidate) != correct_meaning
        }
        if len(eligible) < 3:
            errors.append(f"#{index} ko-jp: fewer than three unambiguous distractors")

    # Quiz/review modes must use the reviewed subset, while the searchable
    # dictionary must retain the complete imported catalogue.
    if "const STUDY_WORDS=WORDS.filter" not in app_source:
        errors.append("app: reviewed study subset is not defined")
    if "const WORD_LIST_WORDS=WORDS" not in app_source:
        errors.append("app: complete dictionary catalogue is not defined")
    if "const list=WORD_LIST_WORDS.filter" not in app_source:
        errors.append("app: dictionary view does not use the complete catalogue")
    unsafe_uses = re.findall(r"(?:shuffle|filter)\(WORDS", app_source[app_source.find("const STORAGE_KEY") :])
    if unsafe_uses:
        errors.append("app: a study path still reads directly from unreviewed WORDS")

    legacy_block = app_source[app_source.find("const LEGACY_WORDS_REVIEWED") : app_source.find("const VOCABULARY_CORRECTIONS")]
    legacy_keys = set(re.findall(r"\{word:'([^']+)'", legacy_block))
    correction_keys = set()
    for start_name, end_name in (
        ("VOCABULARY_CORRECTIONS", "VERB_MEANING_CORRECTIONS"),
        ("KATAKANA_CORRECTIONS", "REVIEWED_WORD_KEYS"),
    ):
        start = app_source.find(f"const {start_name}")
        end = app_source.find(f"const {end_name}", start)
        correction_keys.update(re.findall(r"'([^']+)'\s*:", app_source[start:end]))
    reviewed_count = len(legacy_keys | correction_keys)

    print(f"entries: {len(words)}")
    print(f"reviewed study entries: {reviewed_count}")
    print(f"quarantined review queue: {len(words) - reviewed_count}")
    print(f"unique words: {len(set(w['word'] for w in words))}")
    print(f"quiz cases checked: {len(words) * 2}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
