#!/usr/bin/env python3
"""Report entries that still require lexical or example review."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path


KANJI = re.compile(r"[\u3400-\u9fff々]")
KATAKANA = re.compile(r"[ァ-ヺー]")
HANGUL = re.compile(r"[가-힣]")
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ一-龯]")


def safe_occurrence(sentence, word):
    start = 0
    while True:
        index = sentence.find(word, start)
        if index < 0:
            return False
        before = sentence[index - 1] if index else ""
        end = index + len(word)
        after = sentence[end] if end < len(sentence) else ""
        script = KANJI if KANJI.search(word) else KATAKANA if KATAKANA.search(word) else None
        if script is None or not (script.fullmatch(before) or script.fullmatch(after)):
            return True
        start = index + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.candidates.read_text(encoding="utf-8"))
    issues = []

    for entry in payload["entries"]:
        imported = entry["imported"]
        word = imported["word"]
        flags = []
        dictionary = entry.get("dictionary")
        if not dictionary:
            flags.append("unmatched")
        else:
            if imported["kana"] != dictionary["kana"]:
                flags.append("reading-differs")
            if dictionary["word"] != word:
                flags.append("orthographic-variant")
        usable_ko = [
            sense["definition"] for sense in entry.get("ko_senses", [])
            if HANGUL.search(sense["definition"]) and not JAPANESE.search(sense["definition"])
        ]
        if not usable_ko:
            flags.append("meaning-needs-review")
        source_examples = imported.get("example") and [imported["example"]] or []
        if not any(safe_occurrence(example, word) for example in source_examples):
            flags.append("source-example-mismatch")
        if not entry.get("examples") and not entry.get("tatoeba_ko_examples"):
            flags.append("example-needs-review")
        if flags:
            issues.append({"word": word, "kana": imported["kana"], "flags": flags})

    counts = Counter(flag for item in issues for flag in item["flags"])
    report = {"total": len(payload["entries"]), "flagged": len(issues), "counts": counts, "entries": issues}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({"total": report["total"], "flagged": report["flagged"], "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
