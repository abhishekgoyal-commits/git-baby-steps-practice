# Sprint Velocity Analysis Agent

## Purpose
Use `tools/sprint-velocity-analysis.py` to calculate sprint velocity from completed story-point values supplied on the command line.

## When to Use
- Use when a user asks for sprint velocity from a set of story-point values.
- Use when the completed story points are already available and no Jira API query is needed.
- Do not use for fetching Jira issues, calculating issue-level completion, or producing a team status report; use `tools/jira-analysis.py` for those workflows.

## Command-Line Usage

Pass one or more completed story-point values as positional arguments:

```powershell
py -3 tools/sprint-velocity-analysis.py 2 5 8
```

The command prints:

```text
Sprint velocity: 15 story points
```

Decimal values are supported:

```powershell
py -3 tools/sprint-velocity-analysis.py 1.5 2.25 0
```

## Input Requirements

- Provide at least one `STORY_POINT` value.
- Values may be integers or decimals.
- Values must be non-negative.
- Treat the values as completed story points for one sprint.
- The script calculates velocity as the sum of all supplied values.
- The script does not fetch Jira data or infer completion from issue status.

## Output Requirements

- Write the result to standard output.
- Report the total using the format `Sprint velocity: N story points`.
- Use a concise numeric result without additional narrative.
- Preserve decimal precision in the calculated total when decimal inputs are used.

## Error Handling

- Missing values should be rejected by the command-line parser.
- Non-numeric values should be rejected by the command-line parser.
- Negative values should be rejected with a clear validation error.
- Invalid input must produce a non-zero exit status.

## Validation Checklist

- [ ] Run `py -3 -m py_compile tools/sprint-velocity-analysis.py`.
- [ ] Verify `py -3 tools/sprint-velocity-analysis.py --help` describes positional story-point inputs.
- [ ] Test integer values and confirm their sum is reported.
- [ ] Test decimal values and confirm the total is reported correctly.
- [ ] Test missing, non-numeric, and negative values and confirm they fail.
