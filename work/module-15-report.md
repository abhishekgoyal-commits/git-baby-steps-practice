# Module 15 Completion Report

## Script Metadata
- Filename: bulk_markdown_processor.py
- Language: Python
- Purpose: Recursively scans a directory for Markdown files, extracts each file's title and simple structural metrics, and writes the results to a JSON summary report for bulk processing workflows.

## Script Contents
```python
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
```

## Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| input_dir | Directory containing the Markdown files to process. | . |
| --pattern | Glob pattern used to select which files to include. | *.md |
| --output | JSON file path where the summary report is written. | bulk_summary.json |

## Test Run Output
```text
Processed 31 file(s) from .
- .github\copilot-instructions.md: 41 words, 0 headings
- .github\prompts\to-creating-instructions.prompt.md: 26 words, 0 headings
- .github\prompts\to-fetch-and-summarize-jira-sprint-data.prompt.md: 25 words, 0 headings
- backlog.md: 1792 words, 32 headings
- instructions\calculate-compound-interest.agent.md: 211 words, 5 headings
- instructions\create-status-report.agent.md: 266 words, 14 headings
- instructions\creating-instructions.agent.md: 165 words, 1 headings
- instructions\fetch-and-summarize-jira-sprint-data.agent.md: 374 words, 0 headings
- instructions\jira-analysis.agent.md: 475 words, 9 headings
- instructions\main.agent.md: 303 words, 9 headings
- instructions\sprint-velocity-analysis.agent.md: 331 words, 8 headings
- instructions\validation-rules.md: 373 words, 9 headings
- modules\walkthrough.md: 200 words, 1 headings
- notes.md: 16 words, 1 headings
- PROJECT_IDEAS.md: 344 words, 11 headings
- project_spec.md: 1204 words, 39 headings
- reports\example.md: 275 words, 6 headings
- reports\instructions.md: 282 words, 7 headings
- reports\template.md: 75 words, 6 headings
- reports\weekly-status-2026-08-16.md: 106 words, 4 headings
- reports\weekly-status-2026-08-19.md: 172 words, 4 headings
- skills\skills.md: 280 words, 5 headings
- TODO.md: 52 words, 4 headings
- work\module-03-report.md: 158 words, 16 headings
- work\module-08-report.md: 1238 words, 43 headings
- work\module-09-report.md: 1796 words, 36 headings
- work\module-10-report.md: 658 words, 11 headings
- work\module-12-report.md: 896 words, 13 headings
- work\module-13-report.md: 131 words, 5 headings
- work\module-14-report.md: 1850 words, 36 headings
- work\module03-task\README.md: 85 words, 3 headings
```