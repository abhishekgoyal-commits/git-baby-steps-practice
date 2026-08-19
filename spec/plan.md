# Implementation Plan: Jira Sprint Progress Dashboard

**Feature**: `001-jira-sprint-dashboard`  
**Plan date**: 2026-08-19  
**Status**: Proposed  
**Source**: `spec/specification.md`, `spec/constitution.md`, `spec/clarify.md`

## Delivery Strategy

Deliver the MVP in vertical slices. Establish the unresolved product and integration decisions first, then build the persistence and metric core, expose a stable backend contract, and finally connect the React dashboard. Each phase ends with a reviewable milestone and executable validation. No phase may introduce Confluence publishing; it remains a future feature boundary.

## Milestone Summary

| Milestone | Outcome | Exit condition |
|---|---|---|
| M0: Decisions Locked | Ambiguities converted into approved rules | Clarification decisions recorded and specification updated |
| M1: Reproducible Foundation | Local stack and CI baseline work | React, Express, PostgreSQL 15, Docker, migrations, and checks run consistently |
| M2: Trusted Data Core | Jira data is collected, normalized, persisted, and calculated | Deterministic fixtures produce correct metrics and idempotent refreshes |
| M3: Backend Contract | Dashboard and operations APIs are secure and stable | Contract tests pass for success, stale, unavailable, partial, and error states |
| M4: Dashboard MVP | Manager can inspect sprint health, workload, and risks | Critical user stories pass end-to-end on desktop and mobile |
| M5: Operational Readiness | Daily automation is observable and recoverable | Scheduling, health, retries, alerts, security checks, and runbooks are complete |
| M6: Release Candidate | MVP is deployable and accepted | All quality gates pass and known exceptions have owners and dates |

## Phase 0: Resolve Specification Decisions

**Goal**: Remove decision-blocking ambiguity before implementation.

### Work items

- Select Jira Cloud or Data Center support, REST API version, authentication scheme, and supported provider scope.
- Define the exact sprint-selection model: explicit sprint ID or deterministic discovery, with one-sprint behavior and no-match/multiple-match handling.
- Define completion statuses/resolutions, reopened/cancelled behavior, excluded issue policy, and issue-count semantics.
- Decide missing/invalid story-point handling, zero-point sprint representation, precision, and data-quality warnings.
- Define blocked signals, dependency resolution status, risk evidence, and overdue date source/timezone/end-of-day behavior.
- Define the workload-risk algorithm, default threshold, configuration owner, and rule versioning.
- Define refresh schedule/timezone, freshness thresholds, on-demand permissions, overlap locking, retry bounds, partial-run behavior, and last-success behavior.
- Define authentication and authorization roles for viewing, refreshing, configuring, and operating the system.
- Define API routes, status codes, response nullability, error categories, risk-list bounds/pagination, and correlation-ID behavior.
- Define database retention, snapshot identity/idempotency key, privacy fields, issue removal behavior, and migration policy.
- Define supported Node/package-manager/browser/Docker versions and CI acceptance environment.
- Remove Confluence side effects from MVP acceptance criteria and record Confluence as a future feature.

### Deliverables

- Updated `spec/specification.md` with decisions resolved.
- Configuration schema and environment-variable reference.
- Metric rule table and source-field mapping table.
- API contract draft, preferably OpenAPI plus representative JSON fixtures.
- Decision log linking each resolved item to the relevant requirement.

### Milestone M0 exit criteria

- No decision-blocking item in `spec/clarify.md` remains unanswered or explicitly deferred with an owner and due date.
- The API, persistence, metric, security, and scheduling designs can be implemented without inventing domain rules.
- Product owner and technical owner approve the MVP boundary.

## Phase 1: Reproducible Project Foundation

**Goal**: Make local development and CI deterministic.

### Work items

- Establish frontend and backend package manifests, lockfiles, scripts, and supported runtime versions.
- Configure React 18 + Vite application shell and Node.js + Express service shell.
- Define environment loading and startup validation without logging secrets.
- Configure Docker Compose for PostgreSQL 15 with health/readiness checks and persistent local storage.
- Add migration tooling and an initial migration workflow.
- Add lint, unit-test, integration-test, and production-build commands for frontend and backend.
- Add CI checks for dependency installation, migrations, tests, linting, builds, and secret scanning.
- Document local startup, configuration, test fixtures, and troubleshooting.

### Milestone M1 exit criteria

- A clean checkout can start PostgreSQL 15 through Docker and apply migrations.
- Frontend and backend start using documented commands and fail clearly on missing required configuration.
- CI runs the required quality checks without machine-specific dependencies.
- Health and readiness endpoints exist for the backend and database dependency.

## Phase 2: Trusted Data and Metrics Core

**Goal**: Build the independently testable domain core before UI work.

### Work items

- Implement the Jira adapter with configured authentication, bounded pagination, timeouts, retry/backoff, rate-limit handling, and provider-error mapping.
- Implement source response validation and normalization for issue identity, status, assignee, points, dates, resolution, sprint, project/board, and blocker evidence.
- Implement the configured sprint-selection and scope rules.
- Create PostgreSQL migrations for refresh runs, normalized issue snapshots, sprint metrics, assignee summaries, and risk evidence as decided in M0.
- Add unique constraints and/or idempotency keys for refresh scope plus source identity.
- Implement metric calculation for planned/completed/remaining points and issue counts, completion percentage, blocked and overdue issues, assignee load, missing data, and calculation metadata.
- Implement refresh orchestration with run lifecycle states, correlation IDs, retry records, diagnostic failure reasons, and transaction boundaries.
- Preserve the last successful snapshot when a later run fails or is partial.
- Add deterministic Jira fixtures covering normal, empty, zero-point, missing-point, unassigned, blocked, overdue, malformed, paginated, duplicate, and provider-failure cases.

### Milestone M2 exit criteria

- Unit tests cover every metric rule and edge case in `spec/specification.md`.
- Adapter integration tests cover pagination, authentication failure, rate limits, transient errors, malformed data, and timeout behavior.
- Running the same fixture twice creates no duplicate snapshot, metric, or normalized record.
- A failed or partial run cannot replace the last successful dashboard snapshot.
- Persisted values include source scope, refresh time, and calculation assumptions.

## Phase 3: Secure Backend Contract

**Goal**: Expose the trusted data through a versioned, protected API.

### Work items

- Implement versioned dashboard read endpoint with sprint metadata, metrics, assignees, risk issues, refresh status, and calculation metadata.
- Implement operational refresh endpoint with authentication, authorization, idempotent triggering, and active-run conflict handling.
- Implement health and readiness endpoints that reveal dependency state without sensitive connection details.
- Implement stable error taxonomy and response shape for configuration, validation, authentication, authorization, provider, stale, unavailable, and internal failures.
- Add request validation, output shaping, safe encoding, bounded risk results, and consistent ISO 8601/numeric types.
- Propagate correlation IDs from request through job, adapter, database, and structured logs.
- Add API contract tests and examples for current, stale, unavailable, partial, unauthorized, and provider-error states.

### Milestone M3 exit criteria

- The frontend can consume the contract without direct Jira or database access.
- Contract tests pass for all documented response and error states.
- Unauthorized users cannot view protected data or trigger refreshes.
- API and logs contain no credentials, tokens, SQL details, or unintended sensitive payloads.

## Phase 4: React Dashboard MVP

**Goal**: Deliver the manager workflow end to end.

### Work items

- Implement the sprint header with sprint identity, reporting period, source scope, refresh status, freshness, and last successful refresh.
- Implement KPI presentation for story points, issue counts, completion percentage, blocked issues, overdue issues, and data-quality indicators.
- Implement stable, accessible assignee summary table with sorting/filtering as required by the approved design and explicit `Unassigned` handling.
- Implement risk issue views for blocked and overdue categories, including combined categories and risk evidence.
- Implement loading, empty, stale, unavailable, integration-error, unauthorized, and partial/diagnostic states according to the API contract.
- Ensure stale and source status labels remain visible whenever stored data is not current.
- Add responsive layout and keyboard/screen-reader behavior for critical workflows.
- Add frontend unit/component tests and browser-level tests for the five user stories.

### Milestone M4 exit criteria

- A manager can determine sprint completion, remaining work, blocked work, overdue work, and team workload from the dashboard.
- The UI never fabricates missing or failed metrics and clearly labels stale data.
- Desktop and mobile acceptance checks pass at the agreed viewport/browser matrix.
- Accessibility checks pass for keyboard navigation, semantic tables, labels, focus states, and status announcements.

## Phase 5: Scheduling and Operational Readiness

**Goal**: Make daily refresh dependable in a real environment.

### Work items

- Implement the agreed daily scheduler and timezone behavior.
- Add concurrency control, leases/locks, restart recovery, cancellation behavior, and abandoned-run handling.
- Configure retry limits, exponential backoff, provider rate-limit behavior, and refresh timeout budgets.
- Add structured operational events and metrics for refresh duration, record counts, failures, retries, stale age, and dependency health.
- Define alert thresholds and ownership for failed refreshes, repeated retries, stale data, authorization failures, and readiness failures.
- Add backup/restore, migration rollout, and rollback procedures for PostgreSQL according to deployment decisions.
- Write operator runbook covering credentials, rotation, re-running jobs, diagnosing stale data, and recovering from partial failures.
- Execute a performance test with the agreed expected and maximum issue volume and concurrent dashboard users.

### Milestone M5 exit criteria

- Daily refresh executes at the approved time and timezone.
- Overlapping runs are prevented or safely coalesced.
- A provider outage produces bounded retries, an observable failed run, and a usable stale dashboard.
- Health, logs, metrics, and alerts support diagnosis without reproducing the issue locally.
- Restore and migration procedures are tested in a disposable environment.

## Phase 6: Release Candidate and Acceptance

**Goal**: Verify the implementation against the constitution and approved specification.

### Work items

- Run full frontend and backend unit, integration, contract, end-to-end, accessibility, performance, and migration test suites.
- Run security review covering secret scanning, dependency findings, authentication/authorization, input validation, output encoding, least privilege, and log inspection.
- Verify deterministic calculations against the approved fixture and manually reconcile a representative Jira sprint.
- Verify idempotency by repeating successful, failed, partial, concurrent, and restarted refresh scenarios.
- Verify Docker-based startup, migration, health, backup, and restore workflows.
- Review API documentation, configuration reference, runbook, and known limitations.
- Record any constitution exceptions with scope, compensating controls, owner, and review date.
- Obtain product acceptance from the Delivery Manager and technical approval from the maintainer.

### Milestone M6 exit criteria

- All required quality gates in `spec/constitution.md` pass.
- Success criteria SC-001 through SC-009 are evidenced or have an approved exception.
- No unresolved P0/P1 defects remain.
- MVP scope excludes Confluence publishing and all listed out-of-scope capabilities.
- Release notes identify deployment prerequisites, configuration, known limitations, and rollback steps.

## Dependency Graph

```text
M0 Decisions Locked
        |
        v
M1 Foundation -----> M2 Trusted Data Core -----> M3 Backend Contract
                                                    |
                                                    v
                                           M4 Dashboard MVP
                                                    |
                                                    v
                                           M5 Operational Readiness
                                                    |
                                                    v
                                           M6 Release Candidate
```

M1 can begin with repository setup while M0 is being finalized, but no metric, persistence, API, or UI behavior should be considered stable until M0 is approved. M2 and M3 may proceed in parallel after the domain rules and persistence contract are agreed, but frontend integration depends on M3.

## Cross-Phase Quality Gates

Every phase change MUST include:

- A traceable link to the relevant specification requirements and constitution principles.
- Automated tests for changed behavior and at least one failure path.
- No secrets in source, bundles, API responses, fixtures, or logs.
- Updated API, migration, configuration, or operational documentation when applicable.
- Evidence that retries and reruns remain idempotent.
- A recorded decision or exception for any requirement that remains unresolved.

## MVP Release Boundary

Included:

- One configured active Jira sprint.
- Daily and approved on-demand refresh.
- PostgreSQL 15 persistence through Docker.
- Sprint KPIs, team-member workload, blocked issues, overdue issues, and stale/error states.
- Secure, versioned backend API and responsive React dashboard.

Excluded:

- Confluence page or comment publishing.
- Multi-sprint trends and cross-project portfolio reporting.
- Slack/email alerts and PDF exports.
- Editing Jira issues from the dashboard.
- Capacity planning or replacement of Jira workflow.

## Primary Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Jira status and custom-field variation | Incorrect metrics or risk flags | Configuration-driven mappings, adapter validation, fixture coverage, and visible data-quality metadata |
| Provider outage or rate limiting | Stale dashboard | Bounded retries, last-success retention, freshness indicators, alerts, and operator runbook |
| Ambiguous sprint or source scope | Inconsistent snapshots | Explicit sprint selection, scope metadata, and fail-closed validation |
| Duplicate refresh execution | Duplicate data or inconsistent state | Database uniqueness, transaction boundaries, and concurrency lock/lease |
| Credential leakage | Security incident | Secret manager/environment-only configuration, redacted logs, scanning, and least privilege |
| Unbounded issue volume | Slow refresh or oversized API response | Expected/max volume decision, pagination, indexes, bounded risk results, and performance testing |
| Hidden personal data retention | Compliance exposure | Field minimization, retention policy, access controls, and deletion/anonymization procedure |
