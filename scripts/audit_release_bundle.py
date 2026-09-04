#!/usr/bin/env python3
"""Audit the first-release bundle containing only reviewed vocabulary data."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "reviewed-words.js"
APP = ROOT / "app.js"
HTML = ROOT / "index.html"
SW = ROOT / "sw.js"
KANA = re.compile(r"[ぁ-ゖァ-ヺー・\s]+")
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ一-龯々]")
KOREAN = re.compile(r"[가-힣]")
REQUIRED = ("word", "kana", "meaning", "type", "example", "translation")
RELEASE_VERSION = 22


def load_bundle():
    text = BUNDLE.read_text(encoding="utf-8")
    return json.loads(text[text.index("[") : text.rindex("]") + 1])


def main():
    words = load_bundle()
    app = APP.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    sw = SW.read_text(encoding="utf-8")
    errors = []

    if len(words) != 1791:
        errors.append(f"bundle count is {len(words)}, expected 1791")
    for index, word in enumerate(words):
        for field in REQUIRED:
            if not str(word.get(field, "")).strip():
                errors.append(f"#{index} {word.get('word', '?')}: empty {field}")
        if not KANA.fullmatch(word.get("kana", "")):
            errors.append(f"#{index} {word.get('word', '?')}: invalid kana")
        if set(word) != set(REQUIRED):
            errors.append(f"#{index} {word.get('word', '?')}: unexpected release fields")
        if ";" in word.get("meaning", "") or "；" in word.get("meaning", ""):
            errors.append(f"#{index} {word['word']}: semicolon in meaning")
        if not JAPANESE.search(word.get("example", "")):
            errors.append(f"#{index} {word['word']}: invalid example")
        if not KOREAN.search(word.get("translation", "")):
            errors.append(f"#{index} {word['word']}: invalid translation")

    pairs = Counter((word["word"], word["kana"]) for word in words)
    for (word, kana), count in pairs.items():
        if count > 1:
            errors.append(f"duplicate word/reading: {word} ({kana})")

    for fragment in (
        "const STUDY_WORDS=REVIEWED_WORDS",
        "const WORD_LIST_WORDS=REVIEWED_WORDS",
        "class=\"card-reading-hint\"",
        "let quizAnswers=[]",
        "function showRecordedAnswer(record,w)",
        "#previousQuestion",
    ):
        if fragment not in app:
            errors.append(f"app missing: {fragment}")
    for required in ("#exampleJp", "#exampleKo"):
        if required not in app:
            errors.append(f"app missing reviewed example output: {required}")
    for required in ('id="exampleJp"', 'id="exampleKo"', 'class="example"'):
        if required not in html:
            errors.append(f"html missing reviewed example output: {required}")
    if 'id="previousQuestion"' not in html:
        errors.append("html missing previous-question control")
    versioned_bundle = f'data/reviewed-words.js?v={RELEASE_VERSION}'
    if versioned_bundle not in html or versioned_bundle not in sw:
        errors.append("reviewed bundle is not versioned in HTML and service worker")
    if f"kimheekyo-n3-v{RELEASE_VERSION}" not in sw:
        errors.append("service-worker cache version was not bumped")

    print(f"release entries: {len(words)}")
    print(f"unique word/readings: {len(pairs)}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
