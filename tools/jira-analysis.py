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