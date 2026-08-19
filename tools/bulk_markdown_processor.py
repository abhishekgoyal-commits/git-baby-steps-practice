#!/usr/bin/env python3
"""Bulk-process Markdown files and write a summary report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def summarize_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = ""
    for line in lines:
        cleaned = line.strip()
        if cleaned.startswith("# "):
            title = cleaned[2:].strip()
            break
    if not title:
        title = path.stem.replace("-", " ").title()

    heading_count = sum(1 for line in lines if line.lstrip().startswith("#"))
    word_count = len(text.split())
    return {
        "file": str(path),
        "title": title,
        "heading_count": heading_count,
        "word_count": word_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process Markdown files in bulk and create a summary report."
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default=".",
        help="Directory containing Markdown files to process. Defaults to the current directory.",
    )
    parser.add_argument(
        "--pattern",
        default="*.md",
        help="Glob pattern for files to include. Default: *.md",
    )
    parser.add_argument(
        "--output",
        default="bulk_summary.json",
        help="Output JSON file for the summary results. Default: bulk_summary.json",
    )
    args = parser.parse_args()

    source_dir = Path(args.input_dir)
    if not source_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {source_dir}")

    files = sorted(source_dir.rglob(args.pattern))
    results = [summarize_markdown(path) for path in files if path.is_file()]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Processed {len(results)} file(s) from {source_dir}")
    for item in results:
        print(f"- {item['file']}: {item['word_count']} words, {item['heading_count']} headings")


if __name__ == "__main__":
    main()
