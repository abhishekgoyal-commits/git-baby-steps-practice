# Specification Implementation Checklist

**Reviewed**: 2026-08-20  
**Specification**: `spec/specification.md`  
**Implementation reviewed**: backend, frontend, Docker Compose, tests, and runbook

## Status Definitions

- **Implemented and verified**: Code exists and an executable check or direct endpoint test confirms the behavior.
- **Partially implemented**: A scaffold or placeholder exists, but the specified behavior is incomplete or returns hard-coded data.
- **Not implemented**: No implementation exists in the current codebase.
- **Unverified**: Some code may exist, but the required behavior has no meaningful test or runtime evidence.

## Current Implementation Baseline

| Surface | Finding |
|---|---|
| Backend | `backend/src/server.js` starts Express and exposes `/api/health` plus a hard-coded `/api/dashboard` scaffold. Configuration, routes, controllers, services, jobs, persistence, and authorization modules are empty. |
| Frontend | React 18 + Vite shell builds and displays a placeholder dashboard. It checks `/api/health`, but does not consume `/api/dashboard` or render real metrics. |
| Database | `docker-compose.yml` defines PostgreSQL 15 with a health check, but there are no migrations, database client, repositories, schema, or persistence code. Docker availability was not verified in the environment. |
| Tests | `backend/tests/metrics.test.js` and `backend/tests/dashboard.test.js` are empty. No meaningful automated requirement coverage exists. |
| Runtime checks | Backend syntax and frontend production build were previously verified. The backend health endpoint returned `status: ok`; no Jira or database behavior was tested. |

## User Stories and Acceptance Scenarios

### User Story 1: View sprint health

**Status**: Partially implemented, not functionally verified.

The frontend renders placeholder completion and remaining-point values as `--`, while the backend returns hard-coded zero/null values. No configured sprint or Jira snapshot is read, no required KPI calculation exists, and no acceptance test seeds or requests a real snapshot.

| Scenario | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| Show sprint name, reporting period, last successful refresh, completion percentage | No | No | Backend only returns `name: Active sprint` and no reporting period or last-success timestamp; frontend does not consume it. |
| Show planned/completed/remaining story points | No | No | Hard-coded placeholder values; no metric service. |
| Show planned/completed/remaining issue counts | No | No | No issue-count fields or calculation. |
| Show 0% with no division error for no completed work | No | No | No calculation engine or zero-point test. |

### User Story 2: Review team workload

**Status**: Not implemented.

No assignee summaries, workload threshold, stable ordering, `Unassigned` grouping, or team table exists. The frontend has no team summary component in the active implementation.

| Scenario | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| One summary row per assignee | No | No | No persisted issues, aggregation, API field, or UI table. |
| Explicit `Unassigned` group | No | No | No assignee processing. |
| Mark workload above configured threshold at risk | No | No | No threshold configuration or risk calculation. |
| Stable ordering for equal workload | No | No | No table or ordering rule. |

### User Story 3: Investigate delivery risk

**Status**: Not implemented.

The risk service file is empty. The frontend only shows a generic placeholder “Delivery risks” metric and no issue list.

| Scenario | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| Blocked count and blocked issue list | No | No | No blocker extraction, risk API, or issue list. |
| Overdue count and overdue issue list | No | No | No due-date calculation or issue list. |
| Combined blocked and overdue issue appears once with both categories | No | No | No risk model. |
| Explicit zero/empty risk state | No | No | No risk view or test. |

### User Story 4: Refresh data safely

**Status**: Not implemented.

The daily refresh job, Jira service, persistence, retry policy, run states, and idempotency behavior are absent. The dashboard response is a hard-coded unavailable message and not a stored snapshot.

| Scenario | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| Scheduled refresh stores timestamped snapshot | No | No | `daily-refresh.job.js` is empty; no database schema or Jira client. |
| Retry failure records readable failed status | No | No | No retry or refresh orchestration. |
| Repeating same source input is idempotent | No | No | No persistence or uniqueness constraints. |
| No successful snapshot shows setup/unavailable state | Partial | No | Hard-coded backend `refresh.status: unavailable`, but no snapshot lookup or UI mapping. |

### User Story 5: Operate securely

**Status**: Partially implemented at scaffold level, not functionally verified.

The current server has no Jira credentials or database connection, so there is no secret leakage in the implemented health slice. However, environment validation, authentication, authorization, least privilege, redaction, and integration security are not implemented.

| Scenario | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| Credentials supplied through environment variables | No | No | `config/env.js` is empty; server only reads `PORT`. |
| Missing configuration returns categorized error | No | No | No configuration validator or error taxonomy. |
| Unauthorized dashboard request is rejected safely | No | No | `/api/dashboard` has no authentication or authorization middleware. |

## Functional Requirements

| ID | Requirement summary | Implemented? | Works? | Evidence / gap |
|---|---|---|---|---|
| FR-001 | Support exactly one configured active sprint | No | No | No sprint configuration or source integration. |
| FR-002 | Limit retrieval to configured project, board, and sprint | No | No | Jira service is empty. |
| FR-003 | Retrieve all required Jira issue fields | No | No | No Jira client or field mapping. |
| FR-004 | Handle zero/multiple active sprint matches | No | No | No sprint discovery/validation. |
| FR-005 | Isolate Jira access in backend adapter | Partial | Unverified | No frontend Jira access exists, but the backend adapter itself is empty and no real access path exists. |
| FR-006 | Calculate planned story points | No | No | Metrics service is empty; dashboard returns zero. |
| FR-007 | Calculate completed story points from configured completion definition | No | No | No status/resolution mapping or calculation. |
| FR-008 | Calculate non-negative remaining points | No | No | No calculation engine. |
| FR-009 | Calculate issue counts using matching scope/completion rules | No | No | No issue data or counts. |
| FR-010 | Calculate capped completion percentage | No | No | Response returns `null`; no division/cap logic. |
| FR-011 | Count overdue incomplete issues using timezone rule | No | No | No dates, timezone, or overdue service. |
| FR-012 | Identify blocked issues from configured signals | No | No | Risk service and Jira service are empty. |
| FR-013 | Aggregate metrics by assignee | No | No | No aggregation or assignee data. |
| FR-014 | Identify high remaining workload using threshold | No | No | No threshold configuration or risk logic. |
| FR-015 | Preserve raw values and calculation assumptions | No | No | No snapshots, metadata, or persistence. |
| FR-016 | Expose versioned dashboard endpoint with required sections | Partial | Partial | `/api/dashboard` exists but is not versioned and omits `assignees`, `riskIssues`, and `calculationMetadata`; values are hard-coded. |
| FR-017 | Validate configuration, query parameters, external responses | No | No | No validators or external response handling. |
| FR-018 | Return stable safe machine-readable API errors | No | No | No error middleware or error taxonomy is wired. |
| FR-019 | Persist runs, snapshots/issues, derived metrics, timestamps in PostgreSQL | No | No | Compose defines a database container only; no client, schema, or migrations. |
| FR-020 | Make refresh persistence idempotent | No | No | No persistence or uniqueness strategy. |
| FR-021 | Use versioned migrations safe for Docker workflow | No | No | No migration tooling or migration files. |
| FR-022 | Retain last successful snapshot after failure and expose staleness | No | No | No refresh runs or snapshot selection. |
| FR-023 | Provide daily and authenticated on-demand refresh | No | No | Refresh job and operation endpoint are absent. |
| FR-024 | Use timeout, bounded retry/backoff, rate-limit handling | No | No | No Jira HTTP client. |
| FR-025 | Record refresh lifecycle status/timestamps/reason | No | No | No refresh orchestration or schema. |
| FR-026 | Prevent partial failures being reported as success | No | No | No partial state model. |
| FR-027 | Emit structured logs with correlation context and no secrets | No | No | Server uses one plain startup log; no job logging or correlation IDs. |
| FR-028 | Display sprint header and refresh metadata | No | No | Frontend title is a static scaffold and does not use dashboard data. |
| FR-029 | Display all required KPIs | No | No | Only three placeholder cards exist; issue counts and risk KPIs are absent. |
| FR-030 | Display assignee table with required columns | No | No | No table implementation. |
| FR-031 | Display/filter detailed blocked and overdue issue list | No | No | No risk issue view. |
| FR-032 | Provide loading, empty, stale, integration-error, unauthorized states | Partial | No | Frontend has a backend health `checking/unavailable` state only; required dashboard states are absent. |
| FR-033 | Label stale/partial values and never fabricate metrics | Partial | Partial | Placeholder cards visibly say integration is pending, but no real stale/partial data contract or UI exists. |
| FR-034 | Keep critical workflows usable on desktop/mobile | Partial | Unverified | CSS has a mobile media query for the scaffold; no critical workflow exists and no responsive test is present. |
| FR-035 | Supply credentials/DB strings via environment/secret manager | Partial | Unverified | Compose uses inline development database credentials and backend has no Jira/DB configuration loader. |
| FR-036 | Keep secrets out of source, bundles, responses, logs | Partial | Unverified | No Jira secrets exist in current code, but Compose contains a development password and no secret scanning is configured. |
| FR-037 | Use least-privilege integration/database permissions | No | No | No Jira identity, database roles, or authorization model. |
| FR-038 | Validate and safely encode user/external data | No | No | No user input, external data validation, or output handling. |
| FR-039 | Expose safe health/readiness for dependencies | Partial | Partial | `/api/health` reports backend process only; no readiness endpoint or PostgreSQL/provider dependency status. |
| FR-040 | Separate Jira collection, metrics, and report publishing services | Partial | Unverified | Empty service files suggest intended boundaries, but no implementation or wiring exists. |
| FR-041 | Keep Confluence publishing disabled in MVP | Implemented and verified | Partial | No Confluence code or publishing endpoint exists; no explicit runtime feature guard is needed yet because publishing is absent. |
| FR-042 | Future Confluence publishing is idempotent/auditable/least-privileged | Not implemented | Unverified | Correctly out of MVP, but no future adapter contract exists. |

## API Contract Expectations

**Status**: Partially implemented, contract not compliant.

The backend exposes `/api/dashboard`, but it is not versioned and returns only `sprint`, `metrics`, and `refresh`. It omits `assignees`, `riskIssues`, and `calculationMetadata`, does not identify a snapshot or source scope, and does not distinguish current/stale/failed data. No OpenAPI contract or contract tests exist.

## Key Entities

**Status**: Not implemented.

`Sprint`, `Jira Issue Snapshot`, `Refresh Run`, `Sprint Metrics`, `Assignee Summary`, and `Risk Issue` are described only in Markdown. There are no database tables, migrations, JavaScript models, repositories, or persistence tests.

## Edge Cases and Clarifications

| Edge case | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| Missing story points rule and warning | No | No | No data normalization or data-quality field. |
| Unassigned issue group | No | No | No issue aggregation. |
| No due date not overdue | No | No | No overdue logic. |
| Completed past-due issue handling | No | No | No completion/overdue logic. |
| Zero planned points without division error | No | No | No calculation path; `null` is hard-coded rather than computed. |
| Pagination/duplicates/status/timezone normalization | No | No | Jira service is empty. |
| Failed refresh preserves stale last-success snapshot | No | No | No persistence or refresh job. |
| Malformed Jira data fails or becomes partial with diagnostics | No | No | No provider validation. |
| MVP excludes multi-sprint/portfolio/notifications/exports/Confluence | Partial | Unverified | Product documents state the boundary; runtime has no excluded features to exercise. |

## Non-Functional Requirements

| Requirement | Implemented? | Works? | Evidence / gap |
|---|---|---|---|
| Performance target under 10 seconds | No | No | No real dashboard query or performance dataset/test. |
| Reliability under Jira failures/rate limits | No | No | No Jira integration or retry behavior. |
| Security/no secrets/least privilege | Partial | Unverified | Basic scaffold has no Jira secret path; security controls are otherwise absent. |
| Modular maintainability | Partial | Unverified | Directory boundaries exist, but most modules are empty and the active server bypasses them. |
| Docker/PostgreSQL reproducibility and migrations | Partial | No | Compose and Dockerfiles exist; Docker was unavailable for verification and migrations do not exist. |
| Accessibility for critical dashboard workflows | No | No | No real workflow or accessibility test; semantic scaffolding is insufficient. |

## Success Criteria

| ID | Criterion | Implemented? | Works? | Evidence / gap |
|---|---|---|---|---|
| SC-001 | Manager can determine sprint completion, remaining work, risks, and workload in one view | No | No | UI is a placeholder with no real metrics, table, or risks. |
| SC-002 | Deterministic fixtures produce correct metrics for edge cases | No | No | Test files are empty and no metric engine exists. |
| SC-003 | Standard dashboard request meets 10-second target | No | No | No real request or performance test. |
| SC-004 | Failed refresh is visible while last success remains clearly stale | No | No | No refresh implementation or stale-state UI. |
| SC-005 | Repeated refresh creates no duplicate side effects | No | No | No refresh persistence; Confluence/Jira writes are absent because out of scope. |
| SC-006 | Automated tests cover required behavior | No | No | Backend test files are empty; no frontend tests or test scripts. |
| SC-007 | No secrets in repository/bundles/API/logs | Partial | Unverified | No Jira credentials are present; Compose includes a development password and no scanning evidence exists. |
| SC-008 | Docker starts PostgreSQL and applies migrations | Partial | No | Compose defines PostgreSQL 15, but Docker was unavailable and no migrations exist. |
| SC-009 | MVP remains one sprint and no Confluence publishing | Implemented at documentation level | Unverified at runtime | Specification and plan define the boundary; no runtime feature set exists beyond the scaffold. |

## Verification Gaps

- Docker is not available in the current environment, so PostgreSQL startup and accessibility were not verified.
- The backend has no `test` script and the two test files are empty.
- No Jira credentials, test project, fixture payloads, or provider contract are configured.
- No database migrations, client, schema, repositories, or integration tests exist.
- No authentication/authorization provider is configured.
- No frontend browser, accessibility, or end-to-end test exists.
- No OpenAPI contract, shared types, configuration schema, or error taxonomy is present.
- No daily scheduler is wired into the running server.

## Overall Result

The implementation is currently at **scaffolding stage**, not MVP stage. The only behavior that is both implemented and meaningfully verified is process startup, the backend health endpoint, and the frontend build. The next implementation priorities are the M0 decisions from `spec/clarify.md`, followed by configuration validation, Jira adapter/normalization, PostgreSQL migrations and persistence, metric calculation, refresh orchestration, the versioned API contract, and real dashboard views.,
