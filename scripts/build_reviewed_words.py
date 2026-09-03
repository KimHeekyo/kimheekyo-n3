#!/usr/bin/env python3
"""Build the first-release vocabulary bundle from the human-reviewed ledger."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "words.js"
REVIEW = ROOT / "data" / "manual-review.json"
OUTPUT = ROOT / "data" / "reviewed-words.js"


def load_words():
    text = SOURCE.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def main():
    words = load_words()
    review = json.loads(REVIEW.read_text(encoding="utf-8"))["entries"]
    if len(words) != len(review):
        raise SystemExit(f"review coverage mismatch: {len(review)} / {len(words)}")

    built = []
    for source in words:
        original = source["word"]
        checked = review.get(original)
        if not checked:
            raise SystemExit(f"missing review: {original}")
        built.append({
            "word": checked.get("word", original),
            "kana": checked.get("kana", source["kana"]),
            "meaning": checked["meaning"],
            "type": checked["type"],
        })

    OUTPUT.write_text(
        "const REVIEWED_WORDS = "
        + json.dumps(built, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"built {len(built)} reviewed words")


if __name__ == "__main__":
    main()
