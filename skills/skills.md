# Tool Skills Library

This file maps repository tools to the instructions that explain when and how to use them.

## Tool-to-Instruction Map

| Tool | Purpose | Matching instruction | Typical use |
|---|---|---|---|
| [`tools/compound_interest.py`](../tools/compound_interest.py) | Calculate final amount and interest from principal, rate, compounding frequency, and years. | [`instructions/calculate-compound-interest.agent.md`](../instructions/calculate-compound-interest.agent.md) | Run compound-interest calculations from validated command-line inputs. |
| [`tools/jira-analysis.py`](../tools/jira-analysis.py) | Fetch Jira issues or load a JSON fixture and generate a Markdown status report. | [`instructions/jira-analysis.agent.md`](../instructions/jira-analysis.agent.md) | Produce sprint health, issue progress, risk, and team-view reports. |
| [`tools/sprint-velocity-analysis.py`](../tools/sprint-velocity-analysis.py) | Sum completed story-point values to calculate sprint velocity. | [`instructions/sprint-velocity-analysis.agent.md`](../instructions/sprint-velocity-analysis.agent.md) | Calculate velocity when story-point values are already available. |

## Shared Processing Instructions

| Instruction | Related files | Purpose |
|---|---|---|
| [`instructions/fetch-and-summarize-jira-sprint-data.agent.md`](../instructions/fetch-and-summarize-jira-sprint-data.agent.md) | [`data_fetcher.py`](../data_fetcher.py), [`report_formatter.py`](../report_formatter.py), [`tools/jira-analysis.py`](../tools/jira-analysis.py) | Define Jira fields, normalization, sprint metrics, assignee grouping, and report requirements. |

## Workflow and Authoring Instructions

| Instruction | Related files | Purpose |
|---|---|---|
| [`instructions/create-status-report.agent.md`](../instructions/create-status-report.agent.md) | [`reports/`](../reports/) | Define the concise Markdown format for stakeholder status reports. |
| [`instructions/creating-instructions.agent.md`](../instructions/creating-instructions.agent.md) | [`instructions/`](../instructions/), [`skills/skills.md`](skills.md) | Explain how to create and maintain project instruction files and this tool library. |
| [`instructions/main.agent.md`](../instructions/main.agent.md) | All tools and instructions | Catalog the available project instructions and their intended usage. |

## Usage Rules

- Load the matching instruction before using a tool for a project task.
- Follow each tool's documented command-line arguments and validation rules.
- Keep credentials in environment variables; never place secrets in commands, fixtures, reports, or this library.
- Update this file when adding a tool or a matching instruction.
- Use relative Markdown links so the library remains portable within the repository.
