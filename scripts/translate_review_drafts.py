#!/usr/bin/env python3
"""Create Korean translation drafts for dictionary senses and examples.

Direct Korean dictionary senses and direct Tatoeba translations are retained.
Only missing fields are machine-translated; the output remains a review draft.
"""

import argparse
import json
import subprocess
import time
from pathlib import Path


SEPARATOR = "00000000133700000000"


def google_translate(texts, source, batch_size=25):
    translated = []
    for offset in range(0, len(texts), batch_size):
        batch = texts[offset : offset + batch_size]
        query = f"\n{SEPARATOR}\n".join(batch)
        for attempt in range(6):
            try:
                process = subprocess.run(
                    [
                        "curl", "-fsSL", "--get",
                        "https://translate.googleapis.com/translate_a/single",
                        "--data-urlencode", "client=gtx",
                        "--data-urlencode", f"sl={source}",
                        "--data-urlencode", "tl=ko",
                        "--data-urlencode", "dt=t",
                        "--data-urlencode", f"q={query}",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=90,
                )
                payload = json.loads(process.stdout)
                combined = "".join(part[0] for part in payload[0])
                parts = [part.strip() for part in combined.split(SEPARATOR)]
                if len(parts) != len(batch):
                    raise ValueError(f"translation boundary mismatch: {len(parts)} != {len(batch)}")
                translated.extend(parts)
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(2 ** attempt)
        print(f"{source}->ko: {min(offset + batch_size, len(texts))}/{len(texts)}")
        time.sleep(0.35)
    return translated


def primary_english(entry):
    if not entry["en_senses"]:
        return ""
    return entry["en_senses"][0]["definition"].split(";", 1)[0].strip()


def choose_example(entry):
    direct = {item["ja"]: item for item in entry.get("tatoeba_ko_examples", [])}
    for linked in entry["examples"]:
        if linked["ja"] in direct:
            item = direct[linked["ja"]]
            return {"ja": item["ja"], "ko": item["ko"], "source": item["source"]}
    if entry["examples"]:
        item = entry["examples"][0]
        return {"ja": item["ja"], "ko": "", "source": "JMdict linked example"}
    if entry.get("tatoeba_ko_examples"):
        item = entry["tatoeba_ko_examples"][0]
        return {"ja": item["ja"], "ko": item["ko"], "source": item["source"]}
    imported = entry["imported"]
    return {"ja": imported["example"], "ko": "", "source": "OpenJLPT fallback"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidates", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/translation-drafts.json"))
    parser.add_argument("--prepare-dir", type=Path)
    parser.add_argument("--finalize-dir", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.candidates.read_text(encoding="utf-8"))

    drafts = []
    meaning_jobs = []
    example_jobs = []
    for entry in payload["entries"]:
        korean_sense = entry["ko_senses"][0]["definition"] if entry["ko_senses"] else ""
        example = choose_example(entry)
        draft = {
            "word": entry["imported"]["word"],
            "meaning": korean_sense.rstrip(". "),
            "meaning_source": "Korean Wiktionary" if korean_sense else "machine draft",
            "example": example["ja"],
            "translation": example["ko"],
            "example_source": example["source"],
        }
        if not draft["meaning"]:
            source = primary_english(entry)
            if not source:
                source = entry["imported"]["meaning"]
            meaning_jobs.append((len(drafts), source))
        if not draft["translation"]:
            example_jobs.append((len(drafts), draft["example"]))
        drafts.append(draft)

    if args.prepare_dir:
        args.prepare_dir.mkdir(parents=True, exist_ok=True)
        manifest = {"drafts": drafts, "jobs": {"en": meaning_jobs, "ja": example_jobs}}
        (args.prepare_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
        )
        for language, jobs in manifest["jobs"].items():
            for batch_index, offset in enumerate(range(0, len(jobs), 25)):
                texts = [text for _, text in jobs[offset : offset + 25]]
                (args.prepare_dir / f"{language}-{batch_index:03}.txt").write_text(
                    f"\n{SEPARATOR}\n".join(texts), encoding="utf-8"
                )
        print(f"prepared {len(meaning_jobs)} meanings and {len(example_jobs)} examples")
        return

    if args.finalize_dir:
        manifest = json.loads((args.finalize_dir / "manifest.json").read_text(encoding="utf-8"))
        drafts = manifest["drafts"]
        for language, jobs in manifest["jobs"].items():
            results = []
            batch_files = sorted(args.finalize_dir.glob(f"{language}-*.json"))
            for response_path in batch_files:
                response = json.loads(response_path.read_text(encoding="utf-8"))
                combined = "".join(part[0] for part in response[0])
                results.extend(part.strip() for part in combined.split(SEPARATOR))
            if len(results) != len(jobs):
                raise ValueError(f"{language} result mismatch: {len(results)} != {len(jobs)}")
            for (index, _), result in zip(jobs, results):
                field = "meaning" if language == "en" else "translation"
                drafts[index][field] = result.rstrip(". ") if field == "meaning" else result
    else:
        if meaning_jobs:
            results = google_translate([text for _, text in meaning_jobs], "en")
            for (index, _), result in zip(meaning_jobs, results):
                drafts[index]["meaning"] = result.rstrip(". ")
        if example_jobs:
            results = google_translate([text for _, text in example_jobs], "ja")
            for (index, _), result in zip(example_jobs, results):
                drafts[index]["translation"] = result

    output = {
        "schema_version": 1,
        "status": "machine-assisted drafts requiring final review",
        "entries": drafts,
    }
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(drafts)} drafts to {args.output}")


if __name__ == "__main__":
    main()
