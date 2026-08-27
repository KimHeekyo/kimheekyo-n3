#!/usr/bin/env python3
"""Validate the offline vocabulary bundle before packaging or deployment."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "words.js"
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

    print(f"entries: {len(words)}")
    print(f"unique words: {len(set(w['word'] for w in words))}")
    print(f"quiz cases checked: {len(words) * 2}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
