# Implementation Tasks: Jira Sprint Progress Dashboard

**Feature**: `001-jira-sprint-dashboard`  
**Task list date**: 2026-08-19  
**Status**: Proposed  
**Source**: `spec/plan.md`, `spec/specification.md`, `spec/constitution.md`, `spec/clarify.md`

## Task Conventions

- **Status** starts as `Not started` and is updated during implementation.
- **Dependencies** identify tasks that must be complete before work begins.
- Each task has acceptance criteria that can be verified by review, an automated check, or a documented decision.
- No task may add Confluence publishing to the MVP.

## M0: Decisions Locked

### TASK-001: Approve MVP boundary

**Status**: Completed  
**Dependencies**: None

Record the product owner and technical owner decision that the MVP is a read-only dashboard for one active Jira sprint with daily refresh. Confirm that Confluence publishing, multi-sprint views, notifications, exports, and Jira editing are excluded.

**Acceptance criteria**:

- The approved MVP boundary is recorded in `spec/specification.md`.
- The out-of-scope list matches the release boundary in `spec/plan.md`.
- Confluence is described only as a future extension point.
- Product and technical approvers are named in the decision record.

**Evidence**: `spec/specification.md` - MVP Boundary Decision

### TASK-002: Select Jira provider contract

**Status**: Not started  
**Dependencies**: TASK-001

Choose Jira Cloud or Data Center support, REST API version, authentication method, supported endpoints, and provider error behavior.

**Acceptance criteria**:

- Supported Jira deployment and API version are documented.
- Required endpoints and fields for sprint and issue retrieval are listed.
- Authentication and token-rotation expectations are documented without embedding secrets.
- Retryable and non-retryable provider errors are mapped to internal error categories.

### TASK-003: Define sprint selection and scope

**Status**: Not started  
**Dependencies**: TASK-002

Choose explicit sprint-ID configuration or deterministic active-sprint discovery and define the project, board, and sprint scope rules.

**Acceptance criteria**:

- The authoritative sprint-selection method is documented.
- Behavior for no match, multiple matches, closed sprint, and changed sprint configuration is defined.
- Every refresh records project, board, sprint, and source-scope identifiers.
- A test case exists for each invalid scope condition.

### TASK-004: Define metric and risk rules

**Status**: Not started  
**Dependencies**: TASK-002, TASK-003

Finalize completion, exclusion, story-point, blocked, overdue, workload-risk, and zero-point sprint rules.

**Acceptance criteria**:

- Completion statuses/resolutions, reopened behavior, and excluded issue policy are explicit.
- Missing, invalid, negative, and fractional story-point behavior is explicit.
- Blocker source fields and evidence rules are explicit.
- Due-date source, timezone, and end-of-day comparison are explicit.
- Workload threshold algorithm, default, unit, and rule version are explicit.
- Zero-point sprint response type and UI label are explicit.

### TASK-005: Define refresh and freshness policy

**Status**: Not started  
**Dependencies**: TASK-003, TASK-004

Define the daily schedule, freshness thresholds, on-demand refresh permissions, retry limits, partial-run behavior, concurrency policy, and last-success behavior.

**Acceptance criteria**:

- Daily execution time and timezone are documented.
- Current, stale, unavailable, failed, and partial states have distinct definitions.
- Partial data cannot replace the last successful dashboard snapshot.
- Overlapping runs, process restarts, and abandoned runs have defined behavior.
- Retry count, timeout, and backoff limits are documented.

### TASK-006: Define security and role model

**Status**: Not started  
**Dependencies**: TASK-001, TASK-002

Define authentication, authorization, service identities, protected routes, and least-privilege permissions.

**Acceptance criteria**:

- Viewer, operator, maintainer, and service permissions are documented or explicitly reduced to the supported roles.
- Dashboard read and refresh-trigger permissions are defined.
- Credential storage, rotation, redaction, and access rules are documented.
- Unauthorized and unauthenticated behavior is defined for every protected endpoint.

### TASK-007: Define API contract and error taxonomy

**Status**: Not started  
**Dependencies**: TASK-004, TASK-005, TASK-006

Create the versioned API contract for dashboard reads, refresh operations, health/readiness, and errors.

**Acceptance criteria**:

- Routes, methods, authentication requirements, parameters, status codes, and response schemas are documented.
- Numeric types, nullability, timestamps, risk-list limits, and pagination behavior are documented.
- Current, stale, unavailable, failed, partial, unauthorized, validation, provider, and internal examples exist.
- Error responses contain stable machine-readable categories and safe human-readable messages.
- Correlation-ID propagation is specified.

### TASK-008: Define persistence, privacy, and runtime compatibility

**Status**: Not started  
**Dependencies**: TASK-003, TASK-004, TASK-005, TASK-006

Finalize database entities, uniqueness, retention, personal-data handling, supported runtimes, package manager, browsers, and Docker versions.

**Acceptance criteria**:

- Tables/entities, relationships, indexes, uniqueness keys, and retention rules are documented.
- Raw issue fields, assignee identifiers, summaries, and audit data have an approved storage policy.
- Issue removal and assignee changes have defined behavior.
- Supported Node.js, package manager/lockfile, browser, Docker, and Compose versions are documented.

### TASK-009: Update specification and decision log

**Status**: Not started  
**Dependencies**: TASK-001 through TASK-008

Apply approved decisions to the specification and maintain a traceable decision log.

**Acceptance criteria**:

- `spec/specification.md` no longer contains unresolved decision-blocking alternatives.
- Each decision from TASK-001 through TASK-008 has an owner, date, and rationale.
- Deferred decisions have an owner and due date.
- M0 milestone approval is recorded.

## M1: Reproducible Foundation

### TASK-010: Establish package and runtime baseline

**Status**: Not started  
**Dependencies**: TASK-008

Create or update frontend and backend manifests, lockfiles, scripts, and runtime configuration for React 18 + Vite and Node.js + Express.

**Acceptance criteria**:

- Frontend and backend install from a clean checkout using the approved package manager.
- Required development, test, lint, and production-build scripts exist.
- Runtime versions are enforced or clearly checked at startup/CI.
- Dependency installation is reproducible from lockfiles.

### TASK-011: Create frontend application shell

**Status**: Not started  
**Dependencies**: TASK-010

Configure the Vite entry point, React 18 root, routing/page shell if needed, and API service boundary.

**Acceptance criteria**:

- The frontend starts in development and produces a production build.
- Browser code has no direct Jira or database dependency.
- API base URL and non-secret client configuration are environment-configurable.
- A placeholder loading/error shell renders without console errors.

### TASK-012: Create backend application shell

**Status**: Not started  
**Dependencies**: TASK-010, TASK-006

Configure Express middleware, startup/shutdown lifecycle, environment validation, request IDs, and safe error handling.

**Acceptance criteria**:

- The backend starts with valid non-secret configuration.
- Missing required configuration produces a categorized failure.
- Request correlation IDs are accepted or generated and included in responses/logs.
- Unhandled errors return the approved safe error shape.
- Credentials and database connection strings never appear in logs.

### TASK-013: Provision PostgreSQL 15 through Docker

**Status**: Not started  
**Dependencies**: TASK-008

Configure Docker Compose, PostgreSQL 15, health checks, readiness behavior, persistent local storage, and safe development defaults.

**Acceptance criteria**:

- PostgreSQL starts through the documented Docker command.
- Health/readiness checks distinguish starting, ready, and unavailable states.
- Credentials are supplied through environment configuration and are not committed.
- A clean environment can connect using the documented database settings.

### TASK-014: Add migration workflow

**Status**: Not started  
**Dependencies**: TASK-013

Select and configure migration tooling and establish forward, status, and test-database migration commands.

**Acceptance criteria**:

- Migrations apply successfully to an empty PostgreSQL 15 database.
- Migration status is inspectable and repeatable.
- Applying migrations twice is safe.
- Migration failures stop the workflow with a diagnostic error.

### TASK-015: Add baseline quality automation

**Status**: Not started  
**Dependencies**: TASK-010 through TASK-014

Configure linting, unit-test execution, integration-test setup, production builds, secret scanning, and CI workflow.

**Acceptance criteria**:

- CI installs dependencies, starts required services, applies migrations, runs tests, lints, builds, and scans secrets.
- Each check fails the pipeline when it fails.
- Local commands and CI commands are documented and consistent.
- A clean checkout passes the baseline pipeline.

### TASK-016: Document local development

**Status**: Not started  
**Dependencies**: TASK-010 through TASK-015

Document prerequisites, environment variables, Docker startup, migrations, test commands, and troubleshooting.

**Acceptance criteria**:

- A new developer can start the stack from the documentation.
- Required variables are listed with safe example values or placeholders.
- No documentation contains real credentials.
- Common startup, migration, and readiness failures have recovery steps.

## M2: Trusted Data Core

### TASK-017: Implement Jira client adapter

**Status**: Not started  
**Dependencies**: TASK-002, TASK-003, TASK-010, TASK-012

Implement provider-specific authentication, request construction, pagination, timeouts, retries, rate-limit handling, and error mapping.

**Acceptance criteria**:

- The adapter requests only the approved project/board/sprint scope and fields.
- Pagination terminates correctly and detects incomplete/truncated responses.
- Timeouts and bounded retries follow the approved policy.
- Authentication, rate-limit, timeout, provider, and malformed-response errors map to approved categories.
- Tests use deterministic fixtures and never require committed credentials.

### TASK-018: Validate and normalize Jira issues

**Status**: Not started  
**Dependencies**: TASK-004, TASK-017

Normalize provider responses into the internal issue snapshot model.

**Acceptance criteria**:

- Required issue identity and scope fields are validated.
- Status, resolution, assignee, points, dates, and blocker evidence follow the approved mappings.
- Duplicate issue records are detected and handled deterministically.
- Missing data produces the approved warning/failure behavior.
- Raw source values and normalization outcomes remain available for audit.

### TASK-019: Create domain and persistence migrations

**Status**: Not started  
**Dependencies**: TASK-004, TASK-005, TASK-008, TASK-014

Create tables and indexes for refresh runs, issue snapshots, metrics, assignee summaries, risk evidence, and calculation metadata.

**Acceptance criteria**:

- The schema represents all approved key entities and relationships.
- Foreign keys and uniqueness constraints enforce snapshot/run integrity.
- Queries needed for the dashboard use appropriate indexes.
- Retention and privacy requirements are implementable from the schema.
- Migration tests pass on a clean PostgreSQL 15 database.

### TASK-020: Implement metric calculation engine

**Status**: Not started  
**Dependencies**: TASK-004, TASK-018

Implement deterministic calculations for KPIs, assignee summaries, risk categories, missing-data indicators, and metadata.

**Acceptance criteria**:

- Planned, completed, remaining, and percentage calculations match approved rules.
- Remaining values never become negative from inconsistent source data.
- Blocked, overdue, workload-risk, unassigned, and combined-risk cases are correct.
- Zero-point sprint behavior matches the approved API/UI representation.
- Calculation metadata includes rule versions, source scope, timezone, threshold, and missing-data counts.
- Unit tests cover every edge case listed in the specification.

### TASK-021: Implement refresh run orchestration

**Status**: Not started  
**Dependencies**: TASK-017 through TASK-020

Coordinate collection, validation, normalization, calculation, persistence, status transitions, retries, and failure diagnostics.

**Acceptance criteria**:

- Runs record correlation ID, trigger type, start/end timestamps, status, counts, retries, and failure reason.
- Successful refreshes atomically publish a complete dashboard snapshot.
- Failed and partial runs do not replace the last successful snapshot.
- Transaction rollback prevents incomplete derived data from being treated as successful.
- Repeating identical input is idempotent.

### TASK-022: Add data-core fixture and integration suite

**Status**: Not started  
**Dependencies**: TASK-017 through TASK-021

Build deterministic Jira and database fixtures for normal and failure scenarios.

**Acceptance criteria**:

- Fixtures cover empty, zero-point, missing-point, unassigned, blocked, overdue, malformed, paginated, duplicate, rate-limit, timeout, and provider-failure cases.
- Adapter, normalization, calculation, persistence, and orchestration tests run without live Jira.
- Tests verify last-success retention after failed and partial runs.
- Tests verify no duplicate records after repeated refreshes.

## M3: Secure Backend Contract

### TASK-023: Implement dashboard read endpoint

**Status**: Not started  
**Dependencies**: TASK-007, TASK-019, TASK-020, TASK-021

Expose the approved versioned dashboard response from the latest successful snapshot.

**Acceptance criteria**:

- Response contains sprint, metrics, assignees, risk issues, refresh, and calculation metadata sections.
- Source scope, snapshot identity, freshness, and last successful refresh are included.
- Current, stale, and unavailable states match the approved contract.
- Results are deterministic for the same snapshot and request.
- Risk results obey the approved limit/pagination behavior.

### TASK-024: Implement refresh operation endpoint

**Status**: Not started  
**Dependencies**: TASK-005, TASK-006, TASK-021, TASK-007

Expose a protected, idempotent way for authorized operators to trigger or inspect refreshes.

**Acceptance criteria**:

- Unauthorized callers are rejected without provider or database details.
- Concurrent refresh behavior follows the approved lock/queue/conflict policy.
- The endpoint returns an operation/run identifier and status without exposing secrets.
- Repeated trigger requests do not create duplicate active runs.
- Provider and validation failures use the approved error categories.

### TASK-025: Implement health and readiness endpoints

**Status**: Not started  
**Dependencies**: TASK-012, TASK-013, TASK-019

Expose safe liveness, readiness, and dependency-state checks.

**Acceptance criteria**:

- Liveness does not require external dependencies unless explicitly approved.
- Readiness reports database and required configuration/provider dependency state.
- Responses contain no credentials, connection strings, SQL, or sensitive provider data.
- Checks use stable status codes and documented response shapes.

### TASK-026: Implement authentication and authorization middleware

**Status**: Not started  
**Dependencies**: TASK-006, TASK-012

Apply the approved identity and role model to API routes and operational actions.

**Acceptance criteria**:

- Protected routes enforce authentication.
- Viewer/operator/maintainer permissions match the approved role matrix.
- Authentication failures and authorization failures are distinguishable and safely logged.
- Service credentials use least privilege and are not exposed to the frontend.
- Middleware tests cover missing, invalid, insufficient, and valid identities.

### TASK-027: Add API validation and error contract tests

**Status**: Not started  
**Dependencies**: TASK-023 through TASK-026

Verify request validation, response shaping, error taxonomy, correlation IDs, safe encoding, and all dashboard states.

**Acceptance criteria**:

- Contract tests cover success, stale, unavailable, failed, partial, unauthorized, validation, provider, and internal states.
- Invalid query/body values are rejected before database or Jira access.
- Responses use approved ISO 8601 timestamps, numeric types, and nullability.
- Error payloads contain stable categories and no secrets or SQL details.
- Correlation IDs can be traced across response and structured log fixtures.

## M4: React Dashboard MVP

### TASK-028: Implement dashboard data service

**Status**: Not started  
**Dependencies**: TASK-023, TASK-027

Create the frontend API client and typed/validated view model for dashboard responses.

**Acceptance criteria**:

- The client calls only the approved backend endpoint.
- HTTP and contract errors map to explicit UI states.
- Current, stale, unavailable, and failed refresh metadata are preserved.
- No secret or provider credential is included in the client bundle.

### TASK-029: Implement sprint header and refresh status

**Status**: Not started  
**Dependencies**: TASK-028

Display sprint identity, reporting period, source scope, refresh state, freshness, and last successful refresh.

**Acceptance criteria**:

- Valid data shows sprint name, reporting period, and last successful refresh time.
- Stale, failed, partial, and unavailable states are visibly labeled.
- Dates/times use the approved locale and timezone behavior.
- Loading and error transitions do not cause layout-breaking content shifts.

### TASK-030: Implement KPI view

**Status**: Not started  
**Dependencies**: TASK-028, TASK-004

Display story-point, issue-count, completion, blocked, overdue, and data-quality metrics.

**Acceptance criteria**:

- All required KPI values are displayed with approved labels and units.
- Zero-point and missing-point behavior matches the approved rules.
- Stale or partial values cannot appear current.
- KPI values are accessible to keyboard and assistive-technology users.

### TASK-031: Implement assignee summary table

**Status**: Not started  
**Dependencies**: TASK-028, TASK-004

Display team-member workload and risk summaries.

**Acceptance criteria**:

- Each assignee appears once with approved columns.
- `Unassigned` is explicit and included.
- Risk status and threshold reason are visible.
- Ordering is stable for equal workload values.
- The table is semantically accessible and usable on agreed desktop/mobile viewports.

### TASK-032: Implement risk issue views

**Status**: Not started  
**Dependencies**: TASK-028, TASK-004

Display blocked and overdue issues with categories and evidence.

**Acceptance criteria**:

- Blocked and overdue lists/counts are visible.
- An issue with both categories appears once with both labels.
- Empty states show explicit zero/empty messaging.
- Issue key, summary, assignee, status, points, dates, and risk evidence follow the approved privacy and response rules.

### TASK-033: Implement complete UI state handling

**Status**: Not started  
**Dependencies**: TASK-029 through TASK-032

Implement loading, empty, stale, unavailable, integration-error, unauthorized, and partial/diagnostic states.

**Acceptance criteria**:

- Every API state has a defined, non-fabricated UI state.
- The last successful snapshot remains distinguishable from the failed refresh.
- Retry or recovery actions appear only when authorized and supported.
- Error messages are readable and do not expose internal details.

### TASK-034: Add responsive and accessible dashboard tests

**Status**: Not started  
**Dependencies**: TASK-033

Validate critical user workflows across the approved viewport, browser, keyboard, and assistive-technology matrix.

**Acceptance criteria**:

- User stories 1 through 5 pass with deterministic API fixtures.
- Desktop and mobile viewport checks pass without overlapping or clipped content.
- Keyboard navigation, focus handling, semantic tables, labels, contrast, and status announcements pass the approved accessibility standard.
- Production build passes with no runtime console errors in the tested workflows.

## M5: Operational Readiness

### TASK-035: Implement daily scheduler

**Status**: Not started  
**Dependencies**: TASK-005, TASK-021

Run the approved refresh job on the configured daily schedule and timezone.

**Acceptance criteria**:

- The scheduler runs at the configured time and creates a refresh run with trigger type `scheduled`.
- Schedule configuration is validated at startup.
- Scheduler failures are logged and do not silently stop future runs.
- Scheduling can be disabled safely for tests and local development.

### TASK-036: Implement refresh concurrency and recovery

**Status**: Not started  
**Dependencies**: TASK-005, TASK-021, TASK-024

Implement locks/leases, overlap handling, cancellation, restart recovery, and abandoned-run cleanup.

**Acceptance criteria**:

- Only the approved number of refreshes can run for the configured scope.
- Overlapping scheduled and on-demand requests follow the approved behavior.
- Process restart does not leave the system permanently blocked.
- Abandoned runs become diagnosable and recoverable after the approved lease/timeout.
- Concurrency tests show no duplicate snapshots or inconsistent published state.

### TASK-037: Add operational telemetry and alerts

**Status**: Not started  
**Dependencies**: TASK-025, TASK-035, TASK-036

Add structured events, metrics, dashboards/alerts, and ownership for operational failures.

**Acceptance criteria**:

- Logs include event name, correlation ID, run ID, status, duration, and safe counts where applicable.
- Metrics cover refresh duration, retries, failures, stale age, record counts, and dependency health.
- Alerts exist for failed refreshes, repeated retries, stale data, authorization failures, and readiness failures at approved thresholds.
- Alert ownership and response expectations are documented.

### TASK-038: Add performance and capacity tests

**Status**: Not started  
**Dependencies**: TASK-023, TASK-034, TASK-037

Measure dashboard and refresh performance using the approved expected/max issue volume and concurrency.

**Acceptance criteria**:

- Test data volume and concurrent-user assumptions are documented.
- The standard dashboard request meets the approved 10-second target and percentile definition.
- Refresh duration, database query latency, response size, and UI render behavior are measured separately.
- Any failure includes a documented bottleneck and remediation owner.

### TASK-039: Create operations and recovery runbook

**Status**: Not started  
**Dependencies**: TASK-035 through TASK-038

Document credentials, refresh operations, stale-data diagnosis, failure recovery, migrations, backup/restore, and rollback.

**Acceptance criteria**:

- An operator can diagnose and rerun a failed refresh without source changes.
- Credential rotation steps do not require committing secrets.
- Backup and restore steps are tested in a disposable environment.
- Migration rollback or forward-fix policy is documented.
- Runbook links to health checks, logs, metrics, alerts, and configuration reference.

## M6: Release Candidate

### TASK-040: Run full verification suite

**Status**: Not started  
**Dependencies**: TASK-022, TASK-027, TASK-034, TASK-038, TASK-039

Run all automated and manual checks against the release candidate.

**Acceptance criteria**:

- Unit, integration, contract, end-to-end, migration, accessibility, performance, lint, and production-build checks pass.
- Deterministic fixture results match approved expected values.
- Successful, failed, partial, concurrent, and restarted refresh scenarios are idempotent and recoverable.
- Docker startup and migrations pass from a clean environment.

### TASK-041: Complete security and privacy review

**Status**: Not started  
**Dependencies**: TASK-026, TASK-027, TASK-037, TASK-039

Review secrets, dependencies, authentication, authorization, validation, encoding, logs, permissions, and data retention.

**Acceptance criteria**:

- Secret scanning finds no credentials in repository, fixtures, bundles, responses, or logs.
- Dependency and container findings are reviewed with no unaccepted critical/high issue.
- Protected routes and least-privilege service access are verified.
- Stored fields and retention behavior match the approved privacy policy.
- Exceptions have scope, compensating controls, owner, and review date.

### TASK-042: Reconcile representative Jira sprint

**Status**: Not started  
**Dependencies**: TASK-040, TASK-041

Run the system against a representative non-production Jira sprint and compare results with an independently calculated reference set.

**Acceptance criteria**:

- The source scope is confirmed as the intended one active sprint.
- KPI, assignee, blocked, overdue, and missing-data results reconcile with the reference set.
- Any discrepancy is classified as source-data behavior, specification defect, or implementation defect.
- No production write or Confluence publication occurs during the reconciliation.

### TASK-043: Resolve release defects and exceptions

**Status**: Not started  
**Dependencies**: TASK-040 through TASK-042

Fix release-blocking findings and document any approved exceptions.

**Acceptance criteria**:

- No unresolved P0/P1 defect remains.
- Every accepted exception has an owner, rationale, compensating control, and review date.
- Regression tests cover every fixed defect.
- Specification, API, configuration, and runbook documentation reflect final behavior.

### TASK-044: Obtain MVP acceptance

**Status**: Not started  
**Dependencies**: TASK-043

Obtain product and technical approval for release.

**Acceptance criteria**:

- SC-001 through SC-009 have evidence or approved exceptions.
- Delivery Manager confirms the dashboard supports sprint-health, workload, risk, and refresh workflows.
- Technical maintainer confirms constitution quality gates pass.
- Release notes include prerequisites, configuration, known limitations, rollback, and support ownership.
- Release candidate is explicitly marked ready for deployment.

## Traceability Summary

| Specification area | Tasks |
|---|---|
| Sprint scope and Jira source | TASK-002, TASK-003, TASK-017, TASK-018, TASK-042 |
| Metric and risk calculations | TASK-004, TASK-018, TASK-020, TASK-030, TASK-031, TASK-032 |
| Persistence and idempotency | TASK-005, TASK-008, TASK-014, TASK-019, TASK-021, TASK-036 |
| API and security | TASK-006, TASK-007, TASK-012, TASK-023 through TASK-027, TASK-041 |
| React dashboard | TASK-011, TASK-028 through TASK-034 |
| Scheduling and operations | TASK-005, TASK-035 through TASK-039 |
| Quality and release | TASK-015, TASK-022, TASK-034, TASK-038, TASK-040 through TASK-044 |
| Confluence boundary | TASK-001, TASK-009, TASK-044 |

## Definition of Done

A task is complete only when:

- Its acceptance criteria are verified and recorded.
- Relevant automated tests pass, including at least one failure path where applicable.
- Documentation, API contracts, migrations, configuration, or runbooks are updated when affected.
- No secrets are introduced into source, fixtures, client bundles, API responses, or logs.
- The change preserves idempotency and the approved MVP boundary.
- The task is traceable to the specification and constitution requirements.,
