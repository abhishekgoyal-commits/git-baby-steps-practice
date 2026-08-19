# Module 10 Completion Report

## Instruction Files
```

    Directory: C:\Workspace\hello-genai\instructions


Mode                 LastWriteTime         Length Name                         
----                 -------------         ------ ----                         
-a----         8/19/2026   1:54 PM           1799 create-status-report.agent.md
-a----         8/19/2026   2:13 PM           1350 creating-instructions.agent.m
                                                  d                            
-a----         8/19/2026   2:24 PM           2632 fetch-and-summarize-jira-spri
                                                  nt-data.agent.md             
-a----         8/19/2026   2:24 PM           1974 main.agent.md                
```

## main.agent.md Contents
```markdown
# Agent Instructions Directory

This directory contains specialized agent instructions for common project tasks.

## Available Instructions

### [create-status-report.agent.md](create-status-report.agent.md)
**Purpose:** Generate concise weekly status reports for stakeholder communication

**Key Specs:**
- Format: Markdown
- Max 20 lines, bullet points only
- Sections: Accomplishments, Blockers, Next Week
- Tone: Professional, metric-focused
- Avoids: Fluff language, vague statements

**Usage:** When creating weekly status updates, sync team progress, or reporting to leadership

### [creating-instructions.agent.md](creating-instructions.agent.md)
**Purpose:** Create and maintain platform-agnostic project instructions and IDE wrappers

**Keywords:** create instruction, update instruction, configure instructions, agent instructions, instruction catalog

**Usage:** When adding, revising, validating, or wiring project instruction files

### [fetch-and-summarize-jira-sprint-data.agent.md](fetch-and-summarize-jira-sprint-data.agent.md)
**Purpose:** Fetch Jira sprint issues and produce deterministic sprint metrics and an assignee summary table

**Keywords:** fetch Jira issues, Jira API, sprint data, format issue data, sprint summary, summary table

**Target:** `data_fetcher.py`, `report_formatter.py`, Jira issue-processing workflows

**Usage:** When retrieving, validating, aggregating, or formatting active-sprint issue data

---

## Adding New Instructions

When creating new instruction files:
1. Use `.agent.md` extension
2. Start with a clear Purpose section
3. Include specific constraints and format requirements
4. Add validation checklist for quality assurance
5. Update this index file with a description and usage note

## Quick Reference

| Instruction | Purpose | Format | Owner |
|---|---|---|---|
| create-status-report | Weekly status reporting | Markdown, ≤20 lines | Project Team |
```

## Sample Instruction
- File: @file:fetch-and-summarize-jira-sprint-data.agent.md 
- Contents:
```markdown
- Use this instruction when fetching Jira issues for one active sprint and converting them into a manager-facing summary table.
- Accept input as a JQL string plus optional `max_results`; read `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN` from environment variables.
- Request only the fields needed for processing: `summary`, `status`, `assignee`, `storyPoints`, and `duedate`.
- Treat the Jira response as a list of issue objects under `payload.issues`; preserve each issue key and its original fields for traceability.
- Require each issue to tolerate missing `fields`, `assignee`, `storyPoints`, `duedate`, or status values without crashing.
- Reject missing Jira email or API token before making a request, and never print or include credentials in logs or output.
- Use the Jira REST search endpoint with a 30-second timeout and surface authentication, rate-limit, network, and HTTP errors as actionable failures.
- Normalize missing story points to `0` and missing assignees to `Unassigned`.
- Count an issue as completed when its lowercased status is `done`, `closed`, or `resolved`.
- Count an issue as blocked when a label contains `blocked`; do not treat unrelated labels as blockers.
- Count an issue as overdue when a valid `duedate` in `YYYY-MM-DD` is earlier than the current date; ignore invalid or absent dates.
- Calculate total, completed, and remaining story points; total, completed, and remaining issue counts; completion percentage; blocked count; and overdue count.
- Calculate completion percentage from story points when total story points are greater than zero; otherwise return `0.0`.
- Round completion percentage to one decimal place and ensure remaining values are total minus completed values.
- Group issues by assignee display name and calculate the same sprint metrics for each group.
- Format the summary table as Markdown with columns `Assignee`, `Planned Points`, `Completed Points`, `Remaining Points`, `Completion`, `Remaining Issues`, `Blocked`, and `Overdue`.
- Include a sprint summary before the table with planned/completed/remaining points, planned/completed/remaining issues, completion percentage, blocked count, and overdue count.
- Sort assignee rows by assignee name, placing `Unassigned` according to normal alphabetical ordering.
- Keep output deterministic, concise, and suitable for stakeholder review; do not include raw API payloads, credentials, or unsupported inferred metrics.
- Validate the empty-issue case, all-completed case, no-completed case, mixed statuses, missing fields, blocked labels, overdue dates, and malformed dates before release.
```