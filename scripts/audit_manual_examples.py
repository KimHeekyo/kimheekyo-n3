#!/usr/bin/env python3
"""Validate the human-reviewed example and Korean translation ledger."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / "data" / "words.js"
EXAMPLES = ROOT / "data" / "manual-examples.json"
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ一-龯々]")
KOREAN = re.compile(r"[가-힣]")


def load_words():
    text = WORDS.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def main():
    words = load_words()
    source_keys = {word["word"] for word in words}
    entries = json.loads(EXAMPLES.read_text(encoding="utf-8"))["entries"]
    errors = []
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
    print(f"source entries: {len(words)}")
    print(f"human-reviewed examples: {len(entries)}")
    print(f"remaining examples: {len(words) - len(entries)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
