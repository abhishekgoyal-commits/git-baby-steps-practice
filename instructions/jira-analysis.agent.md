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
