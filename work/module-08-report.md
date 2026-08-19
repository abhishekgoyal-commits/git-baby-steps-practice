# Module 08 Completion Report

## Tracked Files
PROJECT_IDEAS.md
notes.md
project_spec.md
work/module03-task/.gitignore
work/module03-task/README.md
work/module03-task/calculator.py
work/module03-task/init_git.ps1
work/module03-task/main.py

## Spec Commit History
b1e2836 (HEAD -> main) Project reporting specification for module 03 task.

## project_spec.md Contents
# Project Specification: Jira Sprint Progress Dashboard for a Delivery Manager

## 1. Overview

This project will build a Jira-based dashboard to help a Delivery Manager monitor the progress of a single active sprint for a team of 25 people working on enhancements.

The dashboard will provide a high-level view of sprint health, highlight known delivery risk, and help the manager quickly assess whether the sprint is likely to meet its goals.

## 2. Business Goal

The manager needs a simple, fast way to answer the following questions:

- Is the sprint on track?
- How much work is complete versus planned?
- Which work is still at risk?
- Are there blocked items that need intervention?
- Are there signs of overload or uneven distribution across the team?

## 3. User and Audience

### Primary user
- Delivery Manager

### Secondary users
- Team leads
- Senior stakeholders (optional future expansion)

## 4. Requirements Summary from Interview

The following requirements were confirmed:

- Scope: one active sprint only
- Focus: sprint visibility and risk detection
- Grouping: by team member
- Primary metric: story points
- Risk signal: blocked issues
- Update frequency: daily
- Data source: Jira only
- Reporting format: live dashboard only
- Implementation preference: not fixed; recommended default is Python + Jira REST API with a lightweight dashboard UI

## 5. Functional Requirements

### 5.1 Dashboard Scope
The solution must display a dashboard for a single active sprint.

### 5.2 Required KPIs
The dashboard must show at least the following:

- Planned story points vs completed story points
- Remaining story points
- Planned issue count vs completed issue count
- Remaining issue count
- Blocked issue count
- Number of overdue items
- Sprint completion percentage

### 5.3 Team-Level View
The dashboard must group work by team member for a manager who is responsible for 25 people.

This provides visibility into:

- who is ahead or behind
- who has a high remaining load
- where capacity imbalance could affect the sprint outcome

### 5.4 Risk Signals
The system must call out issues that require intervention, including:

- blocked issues
- overdue tasks
- team members with unusually high remaining workload

### 5.5 Daily Refresh
The dashboard should refresh daily to support a manager’s operational decision-making.

## 6. Non-Functional Requirements

### 6.1 Performance
- Dashboard data should refresh within a reasonable time window for daily management reporting.
- A target under 10 seconds for a standard sprint query is desirable.

### 6.2 Reliability
- The solution should gracefully handle Jira API rate limits and temporary connectivity issues.
- Failures should surface readable error messages in logs.

### 6.3 Security
- Jira credentials must be stored securely.
- No secrets should be committed to source control.
- Recommended approach: environment variables or a secure secret manager.

### 6.4 Maintainability
- Code should be modular.
- Jira query logic should be separated from dashboard rendering logic.
- Clear logging should support troubleshooting and future enhancement.

## 7. Data Requirements

### 7.1 Jira Data Needed
The dashboard needs data from the Jira issue model, including:

- issue key
- issue summary
- issue status
- issue assignee
- issue type
- sprint association
- story points
- created date
- due date or target date
- issue resolution status
- blocked or dependency fields
- project key or board association

### 7.2 Derived Data
The system should calculate:

- completed story points
- remaining story points
- completed issue count
- remaining issue count
- completion percentage
- overdue issue count
- blocked issue count
- per-assignee load overview

## 8. Recommended Solution Architecture

### 8.1 Recommended Implementation
Because the user was unsure about the tooling, the recommended default is:

- Python for data retrieval and processing
- Jira REST API for issue access
- Lightweight HTML dashboard or web page for visualization

This approach is flexible, easy to automate, and suitable for a delivery management dashboard without requiring a full enterprise BI stack.

### 8.2 High-Level Components

1. Jira Data Collector
   - Connects to Jira using API authentication
   - Retrieves active sprint issues and relevant fields
   - Filters based on sprint, project, and team membership

2. Data Processor
   - Aggregates issue data
   - Computes sprint metrics
   - Detects overrun, overdue, and blocked work
   - Produces summary values by team member

3. Dashboard Layer
   - Renders a manager-friendly summary view
   - Displays KPIs and risk indicators
   - Presents tables or cards by assignee

4. Configuration Layer
   - Stores Jira URL, project key, sprint name/ID, and credentials via environment variables

## 9. Functional Use Cases

### 9.1 Sprint Health Check
The manager can view:

- total planned story points
- completed story points
- remaining story points
- sprint completion percentage

### 9.2 Blocked Work Review
The manager can identify:

- blocked issues in the active sprint
- whether these items are concentrated in one area or across many team members

### 9.3 Overdue Work Tracking
The manager can identify:

- issues that have passed planned completion windows
- items that are likely to pull the sprint off track

### 9.4 Assignee Load Review
The manager can see:

- how many story points remain per person
- whether any team member has a disproportionate load

## 10. Dashboard Layout Proposal

### Top Row
- Sprint completion %
- Planned vs completed story points
- Planned vs completed issue count
- Blocked issues count
- Overdue items count

### Middle Section
- Team member summary table
  - Assignee
  - Planned points
  - Completed points
  - Remaining points
  - Blocked items
  - Overdue items

### Bottom Section
- Detailed issue list by risk category
  - blocked issues
  - overdue issues
  - at-risk team members

## 11. Acceptance Criteria

The solution will be considered complete when:

1. It successfully connects to Jira for the configured sprint.
2. It retrieves and aggregates required sprint data.
3. It calculates planned, completed, remaining, overdue, and blocked metrics.
4. It shows team member-level summaries.
5. It highlights blocked and overdue work visibly.
6. It refreshes daily without manual intervention.
7. It is secure and does not expose credentials in source code.

## 12. Risks and Constraints

### Risks
- Jira data may be incomplete or inconsistently labeled.
- Story points may not be used uniformly across all issues.
- Some tasks may be carried over from previous sprints.

### Constraints
- Single sprint focus for initial version
- Jira-only data source for version 1
- Limited to daily refresh for initial implementation

## 13. Future Enhancements

After the initial dashboard is working, future versions could include:

- multi-sprint trend reporting
- cross-project portfolio view
- integration with Confluence for release notes and decision logs
- Slack or email alerts for at-risk work
- manager export to PDF or weekly report format

## 14. Recommendation

The strongest initial product is a manager-focused Jira sprint dashboard that:

- covers one active sprint
- groups work by team member
- uses story points as the main tracking metric
- highlights blocked and overdue work
- refreshes daily
- is built with Python and Jira REST API

This provides immediate operational value while remaining simple enough to deliver in a focused first iteration.
