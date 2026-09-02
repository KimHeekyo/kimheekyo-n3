#!/usr/bin/env python3
"""Validate the human-reviewed override ledger."""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORDS = ROOT / "data" / "words.js"
REVIEW = ROOT / "data" / "manual-review.json"
ALLOWED_TYPES = {
    "명사", "동사", "형용사", "부사", "감탄사", "접속사", "관형사", "대명사",
    "조사", "표현", "명사·부사", "명사·형용사", "대명사·부사", "감탄사·형용사",
}


def load_words():
    text = WORDS.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def main():
    words = load_words()
    source_keys = {word["word"] for word in words}
    review = json.loads(REVIEW.read_text(encoding="utf-8"))["entries"]
    errors = []
    for key, entry in review.items():
        if key not in source_keys:
            errors.append(f"unknown source key: {key}")
        if not entry.get("meaning", "").strip():
            errors.append(f"{key}: empty meaning")
        if entry.get("type") not in ALLOWED_TYPES:
            errors.append(f"{key}: invalid type {entry.get('type')!r}")
        if ";" in entry.get("meaning", "") or "；" in entry.get("meaning", ""):
            errors.append(f"{key}: semicolon in meaning")
        senses = [value.strip() for value in entry.get("meaning", "").split(",")]
        if len(senses) != len(set(senses)):
            errors.append(f"{key}: duplicate meaning")
        if entry.get("type") == "동사" and any(
            value and not value.endswith("다") for value in senses
        ):
            errors.append(f"{key}: verb meaning is not in dictionary form")
    print(f"source entries: {len(words)}")
    print(f"human-reviewed meanings: {len(review)}")
    print(f"remaining meanings: {len(words) - len(review)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
