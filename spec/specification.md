# Feature Specification: Jira Sprint Progress Dashboard

**Feature Branch**: `001-jira-sprint-dashboard`  
**Created**: 2026-08-19  
**Status**: Draft  
**Input**: `project_spec.md` and `spec/constitution.md`

## Overview

Build a manager-focused dashboard that retrieves data for one active Jira sprint, calculates sprint health and delivery risk, and presents the results by team member. The initial release is a read-only live dashboard with a daily refresh. The system uses a React 18 + Vite frontend, a Node.js + Express backend, and PostgreSQL 15 running through Docker.

The architecture MUST keep integration and business logic in the backend so a later release can publish approved reports or decision records to Confluence without coupling Confluence behavior to the dashboard UI. Confluence publishing is explicitly out of scope for this release.

## User Scenarios & Testing

### User Story 1 - View sprint health

**Priority**: P1  
**As a** Delivery Manager,  
**I want** to see the current health of the active sprint,  
**so that** I can quickly determine whether delivery is on track.

**Independent Test**: Seed a sprint snapshot containing planned and completed issues, request the dashboard, and verify that all required KPI values and the refresh timestamp are displayed.

**Acceptance Scenarios**:

1. **Given** a configured active sprint with valid Jira data, **When** the manager opens the dashboard, **Then** the dashboard shows the sprint name, reporting period, last successful refresh time, and completion percentage.
2. **Given** planned and completed story-point totals, **When** the dashboard loads, **Then** it shows planned, completed, and remaining story points.
3. **Given** planned and completed issue counts, **When** the dashboard loads, **Then** it shows planned, completed, and remaining issue counts.
4. **Given** a sprint with no completed work, **When** the dashboard loads, **Then** completion is shown as 0% and no division error occurs.

### User Story 2 - Review team workload

**Priority**: P1  
**As a** Delivery Manager,  
**I want** to compare remaining work across team members,  
**so that** I can identify overload and uneven distribution early.

**Independent Test**: Seed issues assigned to multiple team members with different story-point totals and verify the summary table is grouped and calculated correctly.

**Acceptance Scenarios**:

1. **Given** issues assigned to multiple team members, **When** the manager views the team summary, **Then** each member appears once with planned, completed, and remaining points.
2. **Given** an unassigned issue, **When** the summary is calculated, **Then** it appears under an explicit `Unassigned` group rather than being omitted.
3. **Given** a member whose remaining workload exceeds the configured risk threshold, **When** the summary is displayed, **Then** that member is marked at risk and the reason is available.
4. **Given** members with equal workload, **When** the table is displayed, **Then** ordering is stable and does not change between identical refreshes.

### User Story 3 - Investigate delivery risk

**Priority**: P1  
**As a** Delivery Manager,  
**I want** blocked and overdue issues called out,  
**so that** I can intervene on work that threatens the sprint goal.

**Independent Test**: Seed blocked, overdue, and normal issues and verify that risk counts and issue details match the source records.

**Acceptance Scenarios**:

1. **Given** issues marked blocked or having a blocking dependency, **When** the dashboard loads, **Then** the blocked count and blocked issue list are visible.
2. **Given** incomplete issues past their due date, **When** the dashboard loads, **Then** the overdue count and overdue issue list are visible.
3. **Given** an issue that is both blocked and overdue, **When** risks are displayed, **Then** it is represented once in the issue data and may be labeled with both risk categories.
4. **Given** no blocked or overdue issues, **When** the dashboard loads, **Then** the risk sections show an explicit zero or empty state.

### User Story 4 - Refresh data safely

**Priority**: P1  
**As a** Delivery Manager,  
**I want** the dashboard to refresh daily and report refresh failures clearly,  
**so that** I can trust the recency and completeness of the information.

**Independent Test**: Run the refresh job against a deterministic Jira fixture, run it twice, and verify that the second run does not duplicate the snapshot or derived records.

**Acceptance Scenarios**:

1. **Given** valid Jira credentials and an active sprint, **When** the scheduled refresh runs, **Then** a timestamped snapshot is stored and becomes available to the dashboard.
2. **Given** a transient Jira rate-limit or connectivity failure, **When** refresh retries are exhausted, **Then** the job records a failed status with a readable reason and the dashboard does not present the failed run as successful.
3. **Given** a successful refresh run, **When** the same source data is processed again, **Then** the result is idempotent and does not create duplicate side effects.
4. **Given** no successful snapshot exists, **When** the manager opens the dashboard, **Then** the UI displays a setup or unavailable state instead of fabricated metrics.

### User Story 5 - Operate securely

**Priority**: P1  
**As a** project maintainer,  
**I want** integration credentials and operational failures handled securely,  
**so that** the system can run without exposing secrets or sensitive data.

**Independent Test**: Run the backend with credentials supplied through environment variables and inspect logs, API responses, and repository contents for secret leakage.

**Acceptance Scenarios**:

1. **Given** credentials supplied through environment variables, **When** the backend starts, **Then** it can connect without credentials appearing in source files or logs.
2. **Given** missing required configuration, **When** the backend starts or a refresh is requested, **Then** it returns a categorized configuration error and does not make an unauthenticated integration request.
3. **Given** an unauthorized dashboard request, **When** the request is received, **Then** the backend rejects it without exposing integration credentials or database details.

## Functional Requirements

### Sprint and source scope

- **FR-001**: The system MUST support exactly one configured active sprint for the MVP.
- **FR-002**: The system MUST retrieve only issues associated with the configured Jira project, board, and active sprint.
- **FR-003**: The system MUST retrieve the issue key, summary, status, assignee, issue type, sprint association, story points, created date, due date or target date, resolution status, blocked or dependency fields, and project or board association.
- **FR-004**: The system MUST identify the active sprint and report a clear configuration or source-data error when none or multiple active sprints match the configured scope.
- **FR-005**: Jira access MUST be isolated in a backend adapter or service and MUST NOT be called directly by the frontend.

### Metrics and risk rules

- **FR-006**: The system MUST calculate planned story points as the sum of story points for all in-scope issues, treating missing story points according to a documented configuration rule.
- **FR-007**: The system MUST calculate completed story points from issues whose status or resolution matches the configured completed definition.
- **FR-008**: The system MUST calculate remaining story points as planned minus completed, never returning a negative value due to inconsistent source data.
- **FR-009**: The system MUST calculate planned, completed, and remaining issue counts using the same scope and completion definition as the story-point metrics.
- **FR-010**: The system MUST calculate sprint completion percentage as completed story points divided by planned story points, expressed as a percentage and capped at 100%.
- **FR-011**: The system MUST count incomplete issues past the applicable due date as overdue using a documented timezone and date comparison rule.
- **FR-012**: The system MUST identify blocked issues from configured blocked statuses, dependency fields, or equivalent Jira signals.
- **FR-013**: The system MUST aggregate planned, completed, remaining points, blocked issue count, and overdue issue count by assignee.
- **FR-014**: The system MUST identify unusually high remaining workload using a configurable threshold and expose the threshold used for the calculation.
- **FR-015**: The system MUST preserve raw source values and calculation assumptions needed to explain every dashboard metric.

### API and persistence

- **FR-016**: The backend MUST expose a versioned dashboard endpoint that returns sprint metadata, KPIs, team summaries, risk issues, refresh status, and calculation metadata.
- **FR-017**: The backend MUST validate configuration, query parameters, and external responses before calculating or persisting data.
- **FR-018**: API errors MUST use stable machine-readable categories and readable messages without exposing secrets, SQL statements, or provider credentials.
- **FR-019**: PostgreSQL 15 MUST persist refresh runs, source snapshots or normalized issue records, derived metrics, and sufficient timestamps for audit and troubleshooting.
- **FR-020**: Refresh persistence MUST use a uniqueness or idempotency strategy so retries cannot duplicate a source snapshot or generated side effect.
- **FR-021**: Schema changes MUST be delivered through versioned migrations and MUST be safe to apply in the Docker-based development workflow.
- **FR-022**: The system MUST retain the last successful snapshot when a later refresh fails and MUST expose the failed refresh status and staleness information.

### Scheduling and reliability

- **FR-023**: The system MUST provide a daily refresh job and a safe, authenticated way to trigger an on-demand refresh for operations and testing.
- **FR-024**: Integration requests MUST use timeouts, bounded retries with backoff, and explicit handling for rate limits and temporary connectivity failures.
- **FR-025**: A refresh MUST record started, succeeded, partially completed, or failed status with timestamps and a diagnostic reason.
- **FR-026**: Partial failures MUST NOT be represented as a fully successful refresh.
- **FR-027**: Jobs MUST emit structured logs with correlation context and MUST NOT log credentials, tokens, or sensitive payloads.

### Frontend experience

- **FR-028**: The React frontend MUST display the current sprint header, refresh status, and last successful refresh time.
- **FR-029**: The frontend MUST display KPI values for story points, issue counts, blocked issues, overdue issues, and sprint completion percentage.
- **FR-030**: The frontend MUST display a team member summary table with planned, completed, remaining, blocked, overdue, and risk status columns.
- **FR-031**: The frontend MUST display a detailed risk issue list grouped or filterable by blocked and overdue categories.
- **FR-032**: The frontend MUST provide loading, empty, stale-data, integration-error, and unauthorized states.
- **FR-033**: The frontend MUST not render fabricated, partial, or stale values without labeling their source status and refresh time.
- **FR-034**: Critical dashboard workflows MUST remain usable on desktop and mobile viewport sizes.

### Security and configuration

- **FR-035**: Credentials and database connection strings MUST be supplied through environment variables or an approved secret manager.
- **FR-036**: Secrets MUST NOT be committed, included in client bundles, returned by APIs, or written to logs.
- **FR-037**: Integration and database permissions MUST follow least privilege.
- **FR-038**: User-supplied values, webhook payloads, callbacks, and external data MUST be validated and safely encoded before use or display.
- **FR-039**: The backend MUST expose health and readiness information sufficient to diagnose unavailable dependencies without revealing sensitive connection details.

### Confluence readiness

- **FR-040**: The backend architecture MUST keep Jira source collection, metric calculation, and report publishing behind separate service boundaries.
- **FR-041**: Confluence publishing MUST remain disabled in the MVP unless explicitly enabled by a future specification and configuration.
- **FR-042**: Future Confluence publication MUST be idempotent, auditable, least-privileged, and traceable to the dashboard snapshot it publishes.

## Key Entities

### Sprint

Represents the configured active sprint, including sprint ID, name, project or board scope, start date, end date, and state.

### Jira Issue Snapshot

A normalized, timestamped representation of an in-scope Jira issue. It includes source identifiers, status, assignee, story points, dates, resolution, dependency signals, and the source refresh run.

### Refresh Run

Records one scheduled or on-demand collection attempt, including correlation ID, trigger type, start and finish times, status, source scope, record counts, retry information, and failure reason when applicable.

### Sprint Metrics

Stores or derives the aggregate KPI values for one sprint and refresh run, including story points, issue counts, completion percentage, blocked count, overdue count, and calculation metadata.

### Assignee Summary

Represents one assignee, including planned, completed, and remaining points, issue counts, blocked and overdue counts, workload risk status, and the threshold used.

### Risk Issue

An in-scope issue with one or more configured risk categories, including blocked, overdue, or high-load association. It retains the source key, summary, assignee, status, points, due date, and risk evidence.

## API Contract Expectations

The exact route may be finalized during planning, but the dashboard read contract MUST contain these logical sections:

```json
{
  "sprint": {},
  "metrics": {},
  "assignees": [],
  "riskIssues": [],
  "refresh": {},
  "calculationMetadata": {}
}
```

The response MUST identify the snapshot used, its source scope, and whether the values are current, stale, unavailable, or based on a failed refresh. The contract MUST use ISO 8601 timestamps and consistent numeric types.

## Edge Cases and Clarifications

- Missing story points MUST follow one documented rule, such as treating them as zero while reporting the missing-data count; they MUST NOT silently distort totals.
- Unassigned issues MUST remain visible in an explicit group.
- Issues without due dates MUST not be counted as overdue.
- Completed issues with a past due date MUST not be counted as overdue unless the product explicitly defines overdue historically.
- A sprint with zero planned story points MUST report completion as not applicable or 0% according to the chosen product rule, without dividing by zero.
- Jira pagination, duplicate issue records, inconsistent status names, and timezone differences MUST be normalized before aggregation.
- A failed refresh MUST leave the last successful dashboard snapshot available but visibly marked stale.
- If Jira returns malformed or incomplete data, the refresh MUST fail or be marked partial with diagnostics rather than silently dropping records.
- The initial release MUST not support multi-sprint comparisons, cross-project portfolio views, Slack or email alerts, PDF exports, or Confluence publishing.

## Non-Functional Requirements

- **Performance**: A standard active-sprint query and dashboard response SHOULD complete within 10 seconds under expected team size and normal provider latency.
- **Reliability**: Temporary Jira failures and rate limits MUST be retried within bounded limits, and failures MUST remain observable.
- **Security**: No secrets in source control, browser bundles, API responses, or logs; external permissions MUST be least-privileged.
- **Maintainability**: Jira query logic, metric calculation, persistence, and rendering MUST remain independently testable modules.
- **Reproducibility**: PostgreSQL 15 MUST run through Docker for local development and CI, with versioned migrations.
- **Accessibility**: Critical metrics, risk states, tables, and error messages MUST be usable with keyboard navigation and assistive technology.

## Success Criteria

- **SC-001**: A Delivery Manager can determine sprint completion, remaining work, blocked work, overdue work, and team workload from one dashboard view.
- **SC-002**: For a deterministic fixture, calculated metrics match expected story-point and issue-count totals, including zero, missing, unassigned, blocked, and overdue cases.
- **SC-003**: A standard dashboard request completes within 10 seconds under expected sprint size and normal Jira availability.
- **SC-004**: A failed refresh is visible with a readable reason, while the last successful snapshot remains clearly identified as stale.
- **SC-005**: Re-running the same refresh input produces no duplicate snapshot, derived record, Jira comment, Confluence page, or other side effect.
- **SC-006**: Automated tests cover business rules, validation, integration failures, idempotency, and critical frontend states.
- **SC-007**: Repository and runtime inspection finds no Jira, Confluence, or database secrets in committed files, client bundles, API responses, or structured logs.
- **SC-008**: The project can start its PostgreSQL 15 dependency and apply schema migrations using the documented Docker workflow.
- **SC-009**: The MVP remains limited to one active Jira sprint and does not publish to Confluence without an explicitly approved future specification.

## Assumptions

- Jira is the authoritative source for sprint issues and delivery status in the MVP.
- The configured Jira project, board, active sprint, completion statuses, blocked signals, and workload threshold are supplied through validated configuration.
- The initial deployment has one team of approximately 25 people.
- Authentication and authorization mechanisms may be finalized during planning, but they must satisfy the constitution's security requirements before production use.
- Confluence is a planned integration boundary, not an MVP data source or output channel.

## Out of Scope

- Multi-sprint trend reporting.
- Cross-project portfolio reporting.
- Slack or email notifications.
- PDF or scheduled report exports.
- Automatic Confluence page or comment publication.
- Editing Jira issues from the dashboard.
- Replacing Jira workflow, status definitions, or team capacity planning systems.
