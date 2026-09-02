#!/usr/bin/env python3
"""Attach directly linked Japanese-Korean Tatoeba examples to review candidates."""

import argparse
import bz2
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


KANJI = re.compile(r"[\u3400-\u9fff々]")
KATAKANA = re.compile(r"[ァ-ヺー]")


def load_sentences(path):
    result = {}
    with bz2.open(path, "rt", encoding="utf-8") as source:
        for row in csv.reader(source, delimiter="\t"):
            if len(row) >= 3:
                result[int(row[0])] = row[2]
    return result


def has_safe_occurrence(sentence, word):
    start = 0
    while True:
        index = sentence.find(word, start)
        if index < 0:
            return False
        before = sentence[index - 1] if index else ""
        after_index = index + len(word)
        after = sentence[after_index] if after_index < len(sentence) else ""
        if KANJI.search(word):
            if not (KANJI.fullmatch(before) or KANJI.fullmatch(after)):
                return True
        elif KATAKANA.search(word):
            if not (KATAKANA.fullmatch(before) or KATAKANA.fullmatch(after)):
                return True
        else:
            return True
        start = index + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", type=Path)
    parser.add_argument("japanese", type=Path)
    parser.add_argument("korean", type=Path)
    parser.add_argument("links", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.candidates.read_text(encoding="utf-8"))
    japanese = load_sentences(args.japanese)
    korean = load_sentences(args.korean)
    japanese_ids = set(japanese)
    korean_ids = set(korean)
    links = defaultdict(list)

    with args.links.open(encoding="utf-8") as source:
        for row in csv.reader(source, delimiter="\t"):
            if len(row) < 2:
                continue
            left, right = int(row[0]), int(row[1])
            if left in japanese_ids and right in korean_ids:
                links[left].append(right)

    by_first = defaultdict(list)
    for index, entry in enumerate(payload["entries"]):
        word = entry["imported"]["word"]
        if word:
            by_first[word[0]].append((index, word))

    matches = defaultdict(list)
    for sentence_id, sentence in japanese.items():
        korean_ids_for_sentence = links.get(sentence_id)
        if not korean_ids_for_sentence:
            continue
        possible = set()
        for char in sentence:
            possible.update(by_first.get(char, ()))
        for index, word in possible:
            if has_safe_occurrence(sentence, word):
                for korean_id in korean_ids_for_sentence:
                    matches[index].append(
                        {
                            "ja": sentence,
                            "ko": korean[korean_id],
                            "ja_id": sentence_id,
                            "ko_id": korean_id,
                            "source": "Tatoeba direct translation",
                        }
                    )

    covered = 0
    for index, entry in enumerate(payload["entries"]):
        candidates = sorted(
            matches.get(index, ()),
            key=lambda item: (len(item["ja"]), len(item["ko"]), item["ja_id"]),
        )
        entry["tatoeba_ko_examples"] = candidates[:8]
        covered += bool(candidates)
    payload["counts"]["with_direct_korean_example"] = covered
    args.candidates.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
