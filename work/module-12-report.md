# Module 12 Completion Report

## Instruction File
- Filename: jira-analysis.agent.md

```markdown
# Jira Analysis Agent

## Purpose
Use `tools/jira-analysis.py` to fetch Jira issues or load a saved Jira response and produce a deterministic Markdown status report for a sprint or project team.

## When to Use
- Use when a user asks for a Jira status report, sprint health summary, team view, or issue progress analysis.
- Use for one JQL-based Jira query or a local JSON fixture containing Jira issues.
- Do not use for calculating velocity from standalone story-point values; use `tools/sprint-velocity-analysis.py` instead.

## Command-Line Usage

Fetch issues from Jira with JQL:

```powershell
py -3 tools/jira-analysis.py --jql "project = GEN AND sprint = 42"
```

Load issues from a JSON list or Jira response object:

```powershell
py -3 tools/jira-analysis.py --issues-file fixtures/issues.json
```

Optional arguments:
- `--max-results N`: Maximum number of Jira issues to fetch; defaults to `50`.
- `--project-name NAME`: Project or team name shown in the report; defaults to `Sprint`.
- `--reporting-period TEXT`: Reporting period shown in the report.
- `--output PATH`: Write the Markdown report to a file instead of stdout.

`--jql` and `--issues-file` are mutually exclusive, and one is required.

## Jira Configuration

For `--jql`, set these environment variables before running the script:

- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

Credentials must remain in environment variables. Never include them in commands committed to documentation, logs, fixtures, or report output.

## Input Requirements

- Jira responses must contain issues under an `issues` key, or the fixture may be a JSON list of issue objects.
- Each issue should preserve its Jira `key` and contain a `fields` object when available.
- Missing fields, assignees, story points, statuses, labels, or due dates must be tolerated by the formatter.
- Story points default to `0`; missing assignees display as `Unassigned`.

## Report Output

The generated Markdown report contains:

- `Summary`: project/team, reporting period, overall status, and executive summary.
- `Key Updates`: completed points, remaining points, and risks/blockers.
- `Metrics`: completion percentage, issue delivery, team capacity, blocked items, and overdue items.
- `Next Steps`: follow-up actions for blocked and overdue work.
- `Team View`: per-assignee story-point completion and remaining issue counts.

The output must not contain raw Jira payloads, credentials, or unsupported inferred metrics.

## Error Handling

- Reject `--max-results` values less than `1`.
- Surface missing Jira credentials before making a request.
- Report unreadable or malformed JSON fixtures as actionable errors.
- Preserve non-zero exit status for configuration, network, HTTP, or input failures.

## Validation Checklist

- [ ] Run `py -3 -m py_compile tools/jira-analysis.py`.
- [ ] Verify `py -3 tools/jira-analysis.py --help` lists the supported arguments.
- [ ] Test a local fixture with empty, completed, incomplete, blocked, overdue, and unassigned issues.
- [ ] Confirm `--output` writes valid Markdown and stdout remains quiet when it is used.
- [ ] Confirm credentials and raw API responses do not appear in output or logs.
```

## Script File
- Filename: jira-analysis.py
- Language: Python

```python
"""Generate a Markdown status report from Jira issues."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_fetcher import fetch_jira_issues
from report_formatter import generate_report_from_issues


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Format Jira issues as a Markdown status report."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--jql", help="JQL query used to fetch Jira issues.")
    source.add_argument(
        "--issues-file",
        type=Path,
        help="JSON file containing a Jira issue list or an object with an 'issues' key.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum number of issues to fetch (default: 50).",
    )
    parser.add_argument(
        "--project-name",
        default="Sprint",
        help="Project or team name shown in the report.",
    )
    parser.add_argument(
        "--reporting-period",
        help="Reporting period shown in the report (defaults to today's date).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write Markdown to this file instead of stdout.",
    )
    return parser


def load_issues(path: Path) -> List[Dict[str, Any]]:
    """Load issues from a JSON list or Jira-style response object."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read issues file '{path}': {exc}") from exc

    issues = payload.get("issues", []) if isinstance(payload, dict) else payload
    if not isinstance(issues, list):
        raise ValueError("Issues file must contain a JSON list or an 'issues' list.")
    return issues


def main(argv: List[str] | None = None) -> int:
    """Fetch or load Jira issues and write the generated report."""
    args = build_parser().parse_args(argv)

    if args.max_results < 1:
        print("error: --max-results must be greater than zero", file=sys.stderr)
        return 2

    try:
        issues = load_issues(args.issues_file) if args.issues_file else fetch_jira_issues(
            args.jql, args.max_results
        )
        report = generate_report_from_issues(
            issues,
            project_name=args.project_name,
            reporting_period=args.reporting_period,
        )
        if args.output:
            args.output.write_text(report + "\n", encoding="utf-8")
        else:
            print(report)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Script Execution Output
```text
usage: jira-analysis.py [-h] (--jql JQL | --issues-file ISSUES_FILE)
                        [--max-results MAX_RESULTS]
                        [--project-name PROJECT_NAME]
                        [--reporting-period REPORTING_PERIOD]
                        [--output OUTPUT]

Format Jira issues as a Markdown status report.

options:
  -h, --help            show this help message and exit
  --jql JQL             JQL query used to fetch Jira issues.
  --issues-file ISSUES_FILE
                        JSON file containing a Jira issue list or an object
                        with an 'issues' key.
  --max-results MAX_RESULTS
                        Maximum number of issues to fetch (default: 50).
  --project-name PROJECT_NAME
                        Project or team name shown in the report.
  --reporting-period REPORTING_PERIOD
                        Reporting period shown in the report (defaults to
                        today's date).
  --output OUTPUT       Write Markdown to this file instead of stdout.
```
