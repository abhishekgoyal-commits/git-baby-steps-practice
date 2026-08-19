# Specification Review: Gaps, Contradictions, and Clarifications

**Reviewed documents**: `spec/constitution.md`, `spec/specification.md`  
**Review date**: 2026-08-19  
**Reviewer stance**: Senior engineering review

## Executive Assessment

The specification is a strong product outline, but it is not yet implementation-ready. The largest unresolved areas are Jira semantics, configuration ownership, authentication, refresh behavior, persistence design, and measurable operational limits. The questions below should be resolved before finalizing the data model, API contract, or implementation plan.

## Decision-Blocking Gaps

### 1. Define the Jira completion model

**References**: FR-007, FR-009, FR-010, FR-011, Edge Cases

The specification alternates between status and resolution as completion signals but does not define which field wins, which values count as completed, or how reopened issues are handled.

**Clarify**:
- Which Jira statuses and/or resolutions represent completed work?
- Is completion based on status category, exact status names, resolution, or a combination?
- Are reopened issues counted as incomplete?
- Are cancelled, duplicate, or rejected issues included in planned work and completion percentages?

**Recommended decision**: Configure an explicit set of completed status IDs and a separate excluded-status policy. Store the effective completion rule in `calculationMetadata` for every snapshot.

### 2. Define missing and invalid story-point behavior

**References**: FR-006, FR-015, Edge Cases, SC-002

Missing points are described as configuration-dependent, with zero offered as an example, but no default or required reporting behavior is selected. Negative, fractional, and non-numeric values are also unspecified.

**Clarify**:
- Are missing points treated as zero, excluded from point totals, or an error?
- Must the dashboard display a missing-points count and warning?
- Are negative or fractional points valid?
- How are issue types without story points handled?

**Recommended decision**: Treat missing points as zero for counts and totals, report `missingStoryPointCount`, reject negative values, and preserve the raw value and normalization outcome.

### 3. Define blocked-issue semantics

**References**: FR-012, User Story 3, Risk Issue entity

“Blocked statuses,” dependency fields, and equivalent signals are named, but the source fields and precedence are not specified. Jira installations commonly represent blocking through linked issues, custom fields, labels, or status values.

**Clarify**:
- Which Jira link type or custom fields indicate a blocker?
- Does a blocked dependency need to be unresolved to count?
- Which status values are blocked?
- What evidence and source field should appear in the risk issue response?

**Recommended decision**: Define a normalized blocker rule with source field, value mapping, and an evidence string per issue; test each supported Jira representation.

### 4. Define overdue dates and timezone

**References**: FR-011, Edge Cases

The specification requires a timezone rule but does not choose one. “Applicable due date” and “past due” are also ambiguous for date-only and timestamp values.

**Clarify**:
- Is overdue evaluated against Jira due date, target date, or a configured fallback order?
- What timezone is authoritative: Jira instance, project, team, user, or UTC?
- Is an issue overdue at the start of the due date, end of the due date, or after the date passes?
- Are due dates in the future sprint window only?

**Recommended decision**: Use the configured Jira/project timezone, compare date-only due dates at end-of-day, and define a documented fallback when no due date exists.

### 5. Define workload-risk threshold

**References**: User Story 2, FR-014, Assumptions

“Unusually high” and “configurable threshold” have no algorithm, unit, default, or owner. A fixed story-point threshold and a relative team comparison produce different results.

**Clarify**:
- Is the threshold an absolute remaining-point value, a percentage of team remaining work, a percentile, or a comparison to average/median?
- What is the default for a 25-person team?
- Are unassigned work and completed work included in the comparison?
- Who may change the threshold and when does it take effect?

**Recommended decision**: Choose one deterministic rule for MVP, such as remaining points greater than a configured absolute threshold, and return both threshold and rule version in metadata.

### 6. Define the configuration and deployment model

**References**: FR-001, FR-002, FR-023, FR-035, Assumptions

The specification says configuration is validated but does not define required variables, ownership, runtime location, or whether configuration changes require a restart or migration.

**Clarify**:
- Which values are required: Jira base URL, project key, board ID, sprint ID, status mappings, timezone, threshold, refresh schedule, database URL, and authentication settings?
- Is the active sprint selected by sprint ID, board lookup, project lookup, or automatic discovery?
- Is configuration global or per tenant/team?
- Which environment owns the scheduled job: backend process, Docker container, host scheduler, or CI?
- How are configuration changes audited and rolled back?

**Recommended decision**: Define a versioned environment/configuration schema and select one authoritative sprint identifier for the MVP.

### 7. Define authentication and authorization

**References**: Constitution IV, User Story 5, FR-023, FR-037, FR-039

“Safe, authenticated” and “unauthorized request” are requirements, but the identity provider, session/token model, roles, and protected routes are absent.

**Clarify**:
- Who can view the dashboard and trigger a refresh?
- What roles exist, and which role can change configuration?
- Is authentication handled by an existing reverse proxy, OAuth/OIDC, JWT, or application sessions?
- How are service-to-service credentials rotated?
- How are authentication failures logged without leaking identity data?

**Recommended decision**: Specify the deployment identity boundary and a minimum role matrix before implementing API middleware.

### 8. Define refresh cadence and freshness

**References**: Overview, User Story 4, FR-023, FR-022, SC-004

The dashboard is called “live,” but the data is refreshed daily and may remain stale after failure. No exact schedule, freshness SLA, stale threshold, or manual refresh interaction is defined.

**Clarify**:
- What time and timezone is the daily refresh scheduled?
- Does “live” mean live UI/API access to the latest stored snapshot or live Jira reads?
- What age makes a snapshot stale, and what age makes it unavailable?
- Can a manager request a refresh from the UI, or only an operator?
- What happens when a refresh overlaps a previous run?

**Recommended decision**: Define “live” as an API over the latest persisted snapshot, set a freshness threshold, and enforce one active refresh per configured scope.

### 9. Define partial-failure semantics

**References**: FR-025, FR-026, FR-022, Edge Cases

A refresh may be “partially completed,” but the specification does not say whether partial records are stored, whether metrics are calculated, or which data the dashboard may show.

**Clarify**:
- Is a partial snapshot queryable?
- Are partial metrics rejected, marked incomplete, or calculated from available records?
- Does a partial run replace the last successful snapshot?
- What minimum completeness is required for success?

**Recommended decision**: Do not replace the last successful snapshot with partial data; retain partial records for diagnostics only and expose a failed/partial run separately.

### 10. Define the persistence and retention model

**References**: FR-019, Key Entities, FR-020, FR-022

The required entities are conceptual, not a schema. Retention, indexes, relationships, uniqueness keys, and deletion/anonymization rules are missing.

**Clarify**:
- What uniquely identifies a refresh snapshot: sprint plus source hash, run ID, or timestamp?
- How long are raw issue snapshots and audit records retained?
- Are historical snapshots required for the MVP or only the latest successful snapshot?
- How are removed Jira issues, assignee changes, and sprint changes represented?
- What indexes are required for dashboard latency?

**Recommended decision**: Define a migration-level data model, retention policy, and unique constraints before persistence implementation.

### 11. Define the external Jira API contract

**References**: FR-003, FR-004, FR-024, User Story 4

The specification requires pagination, normalization, retries, and rate-limit handling but does not define Jira Cloud versus Data Center, API version, endpoint strategy, page limits, or provider error mapping.

**Clarify**:
- Is the target Jira Cloud, Jira Data Center, or both?
- Which REST API version and authentication scheme are supported?
- What is the maximum expected issue count?
- Which provider errors are retryable, and what are the retry/backoff limits?
- How are pagination truncation and provider schema changes detected?

**Recommended decision**: Name the supported Jira deployment/API version and define an adapter contract with provider errors mapped to internal categories.

### 12. Define the API surface and response schema

**References**: FR-016, API Contract Expectations

Only logical response sections are provided. The route, HTTP methods, status codes, query parameters, field types, nullability, pagination, and error schema are deferred to planning even though the constitution requires explicit contracts.

**Clarify**:
- What are the exact dashboard, refresh, health, and readiness routes?
- Is risk issue data paginated or bounded?
- Are numeric values integers, decimals, or nullable?
- What HTTP status and error payload are returned for unavailable, stale, partial, unauthorized, and provider-failure states?
- Is a dashboard request scoped by sprint, project, or configuration only?

**Recommended decision**: Add an OpenAPI or equivalent contract before implementation, including examples for all required UI states.

## Contradictions and Tensions

### 13. “Live dashboard” versus daily stored snapshots

**References**: Overview, project intent, FR-022, FR-023

The product is described as a live dashboard, but the architecture is snapshot-based with daily refreshes and stale-data behavior. These are compatible only if “live” means live access to the latest persisted snapshot.

**Resolve**: Explicitly define the dashboard as a live view of persisted data. State whether on-demand refresh is user-visible and whether the UI ever reads Jira directly.

### 14. Jira-only MVP versus Confluence automation scope

**References**: project scope, Overview, FR-040 to FR-042, SC-005

The source specification says Jira only and live dashboard only, while the constitution and specification title describe Jira/Confluence automation and SC-005 mentions Confluence pages. This can lead implementers to build or test an out-of-scope publishing path.

**Resolve**: Keep Confluence as an architectural extension point only, remove Confluence side effects from MVP acceptance tests, and move future publication requirements to a separate feature specification.

### 15. “No duplicate side effects” when MVP is read-only

**References**: Overview, FR-020, SC-005

A read-only dashboard has no Jira comments or Confluence pages to duplicate. SC-005 includes those side effects even though publishing is explicitly out of scope.

**Resolve**: For MVP, test duplicate-free refresh runs, snapshots, and derived records only. Reserve external publication idempotency for the future Confluence feature.

### 16. Partial status versus last successful snapshot

**References**: FR-022, FR-025, FR-026

The system must record partial runs but must not represent them as successful. It is unclear whether the partial result can be shown, and this conflicts with the requirement not to show fabricated or partial values.

**Resolve**: Define partial data as diagnostics-only and keep the last successful snapshot as the only dashboard data source.

### 17. Missing-point handling versus “planned points” definition

**References**: FR-006, FR-008, Edge Cases

If missing points are treated as zero, planned issue count and planned points describe different populations. If missing-point issues are excluded, the dashboard can understate planned work. The specification does not define how the discrepancy is surfaced.

**Resolve**: Add explicit missing-data KPIs and a visible data-quality warning, or define a strict validation failure for missing points.

### 18. Constitution auditability versus read-only MVP

**References**: Constitution VI, specification Overview, FR-015

The constitution requires manual override history, but the specification makes the dashboard read-only and does not define overrides. This is a governance requirement without an in-scope feature or data model.

**Resolve**: State that manual overrides are not supported in MVP and that the audit requirement applies to source snapshots and calculation metadata only until an override feature is specified.

### 19. “Exactly one active sprint” versus zero or multiple matches

**References**: FR-001, FR-004

FR-001 says exactly one configured active sprint, while FR-004 describes none or multiple matches as runtime conditions. It is unclear whether the system discovers the sprint or trusts a configured ID.

**Resolve**: Choose either explicit sprint-ID configuration or automatic discovery with a deterministic selection rule; do not combine both without precedence.

### 20. “All required KPI values” versus zero-point sprint behavior

**References**: User Story 1, FR-010, Edge Cases

The acceptance scenario requires a completion percentage, while the edge case allows either “not applicable” or 0% when planned points are zero. Those are different API types and UI behaviors.

**Resolve**: Select one representation, preferably `completionPercentage: null` with `completionStatus: "not_applicable"` and a clear UI label.

## Cross-Cutting Unclear Requirements

### 21. Error taxonomy and observability

The specification requires machine-readable errors and structured logs but does not list categories, correlation-ID propagation, log retention, alert ownership, or user-facing versus operator-facing details.

**Questions**: Define categories such as `CONFIGURATION_ERROR`, `AUTHENTICATION_ERROR`, `AUTHORIZATION_ERROR`, `PROVIDER_RATE_LIMIT`, `PROVIDER_UNAVAILABLE`, `VALIDATION_ERROR`, and `DATA_STALE`; specify correlation behavior and retention.

### 22. Test strategy and acceptance environment

The document names deterministic fixtures but does not identify the test framework, database isolation strategy, browser test tool, Jira contract fixtures, or performance-test dataset.

**Questions**: Which checks are unit, integration, contract, end-to-end, and performance tests? Must CI start Docker? What fixture size represents the expected 25-person sprint?

### 23. Frontend usability and accessibility criteria

“Usable on desktop and mobile” and “usable with assistive technology” are not measurable. No viewport targets, keyboard behavior, table semantics, color contrast, or screen-reader announcements are defined.

**Questions**: Which viewport sizes and browsers are supported? What accessibility standard is required? How are loading, stale, and error transitions announced?

### 24. Data privacy and retention

The documents require minimizing sensitive data but do not identify whether issue summaries, assignee names, account IDs, or audit data are personal data, nor how long they may be retained.

**Questions**: What fields may be persisted? What deletion or retention policy applies? Are assignee display names stable identifiers, and how are departed users handled?

### 25. Capacity and performance limits

The 25-person team size does not define issue count, concurrent users, refresh duration, payload size, or database growth assumptions. The 10-second target does not specify percentile, environment, or whether Jira latency is included.

**Questions**: Define expected and maximum issue counts, concurrent dashboard users, performance percentile, and whether the 10-second target covers refresh, API response, UI render, or only a standard read request.

### 26. Time and localization behavior

ISO 8601 is required for the API, but the UI display locale, timezone, date-only interpretation, daylight-saving behavior, and clock source are not specified.

**Questions**: Should the UI use the browser timezone or configured project timezone? Which locale and number precision should be used for story points and percentages?

### 27. Configuration and version compatibility

The stack is named as React 18, Vite, Node.js, Express, and PostgreSQL 15, but supported minor versions, Node runtime policy, package manager, browser support, and Docker Compose version are absent.

**Questions**: Define supported runtime versions and lockfile/package-manager policy so local and CI environments are reproducible.

### 28. Refresh concurrency and cancellation

The requirements address retries and idempotency but not concurrent scheduled/manual runs, process restarts, cancellation, or lock expiry.

**Questions**: What happens if a scheduled run starts while an on-demand run is active? Is there a database advisory lock, queue, or lease? How are abandoned runs recovered?

### 29. Jira changes during collection

The specification does not define consistency when issues change while pagination is in progress or when the sprint starts/ends during collection.

**Questions**: Is the collection best-effort or based on a provider snapshot? Are start/end timestamps captured and used to define scope? How are duplicate or changed records reconciled?

### 30. Deployment and disaster recovery

Docker is required for PostgreSQL development and CI, but production topology, backups, migrations during deployment, restart behavior, and recovery objectives are absent.

**Questions**: Where do frontend, backend, and database run in production? Who operates backups? What are the required recovery point and recovery time objectives?

## Recommended Clarification Order

1. Choose Jira deployment/API/authentication model and define source-field mappings.
2. Resolve metric rules: completion, missing points, blocked status, overdue timezone, and workload risk.
3. Decide sprint selection, refresh freshness, partial-failure, concurrency, and last-success behavior.
4. Define the persistence schema, retention, idempotency key, and migrations.
5. Publish the exact API/error contract and authentication/authorization matrix.
6. Define test, accessibility, performance, deployment, and data-retention acceptance thresholds.
7. Remove Confluence side effects from MVP criteria and create a separate future publishing specification.

## Review Conclusion

The specification should remain in Draft status until the first seven clarification groups are answered. Once those decisions are recorded, the implementation plan can be decomposed safely without guessing at Jira semantics, data integrity, security boundaries, or stale/partial dashboard behavior.,
