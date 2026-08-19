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

### [jira-analysis.agent.md](jira-analysis.agent.md)
**Purpose:** Use `tools/jira-analysis.py` to fetch or load Jira issues and generate a Markdown status report

**Keywords:** Jira analysis, Jira status report, sprint health, issue progress, team view

**Usage:** When running the Jira analysis CLI or documenting its inputs, outputs, and validation

### [sprint-velocity-analysis.agent.md](sprint-velocity-analysis.agent.md)
**Purpose:** Use `tools/sprint-velocity-analysis.py` to calculate sprint velocity from completed story-point values

**Keywords:** sprint velocity, completed story points, velocity calculation, sprint metrics

**Usage:** When calculating or documenting velocity from a supplied set of story-point values

---

## Adding New Instructions

When creating new instruction files:
1. Use `.agent.md` extension
2. Start with a clear Purpose section
3. Include specific constraints and format requirements
4. Add validation checklist for quality assurance
5. Update this index file with a description and usage note

---

## Quick Reference

| Instruction | Purpose | Format | Owner |
|---|---|---|---|
| create-status-report | Weekly status reporting | Markdown, ≤20 lines | Project Team |
