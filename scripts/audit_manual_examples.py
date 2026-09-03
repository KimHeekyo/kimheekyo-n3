#!/usr/bin/env python3
"""Validate the human-reviewed example and Korean translation ledger."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / "data" / "words.js"
EXAMPLES = ROOT / "data" / "manual-examples.json"
REVIEW = ROOT / "data" / "manual-review.json"
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ一-龯々]")
KOREAN = re.compile(r"[가-힣]")


def appears_in_example(word, kana, word_type, example):
    """Conservatively accept a headword, reading, or common inflectional stem."""
    candidates = {word, kana}
    if word_type == "동사" and len(word) > 1:
        candidates.add(word[:-1])
    if word_type == "형용사" and word.endswith("い") and len(word) > 1:
        candidates.add(word[:-1])
    return any(candidate and candidate in example for candidate in candidates)


def load_words():
    text = WORDS.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def main():
    words = load_words()
    source_keys = {word["word"] for word in words}
    source_by_key = {word["word"]: word for word in words}
    reviews = json.loads(REVIEW.read_text(encoding="utf-8"))["entries"]
    entries = json.loads(EXAMPLES.read_text(encoding="utf-8"))["entries"]
    errors = []
    warnings = []
    seen_examples = {}
    for key, entry in entries.items():
        example = entry.get("example", "").strip()
        translation = entry.get("translation", "").strip()
        if key not in source_keys:
            errors.append(f"unknown source key: {key}")
        if not example or not JAPANESE.search(example):
            errors.append(f"{key}: invalid Japanese example")
        if not translation or not KOREAN.search(translation):
            errors.append(f"{key}: invalid Korean translation")
        if ";" in example + translation or "；" in example + translation:
            errors.append(f"{key}: semicolon found")
        if example and example[-1] not in "。！？!?":
            errors.append(f"{key}: Japanese sentence has no terminal punctuation")
        if translation and translation[-1] not in ".?!다요죠까자라네어아임됨음함":
            errors.append(f"{key}: Korean sentence has no terminal punctuation")
        if example in seen_examples:
            errors.append(f"{key}: duplicate example also used by {seen_examples[example]}")
        seen_examples[example] = key
        if key in source_by_key and key in reviews:
            source = source_by_key[key]
            review = reviews[key]
            word = review.get("word", key)
            kana = review.get("kana", source.get("kana", ""))
            if not appears_in_example(word, kana, review["type"], example):
                warnings.append(f"{key}: headword occurrence needs manual confirmation")
    print(f"source entries: {len(words)}")
    print(f"human-reviewed examples: {len(entries)}")
    print(f"remaining examples: {len(words) - len(entries)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    print(f"manual occurrence warnings: {len(warnings)}")
    for warning in warnings:
        print(f"- {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
