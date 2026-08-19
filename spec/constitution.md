# Jira/Confluence Automation Constitution

**Version:** 1.0.0  
**Ratified:** 2026-08-19  
**Last Amended:** 2026-08-19

## Purpose

This constitution defines the engineering principles and quality gates for the Jira/Confluence automation project. It governs feature design, implementation, review, and operational changes across the React frontend, Node.js backend, and PostgreSQL data layer.

## Principles

### I. Outcome-Driven Automation

Automations MUST solve a documented delivery-management need and MUST define their inputs, outputs, owner, and failure behavior. Jira and Confluence content MUST be treated as operational records: generated updates must be traceable to source data, reproducible for the same inputs, and clearly distinguish facts from derived conclusions.

### II. Clear Ownership by Layer

The React 18 + Vite frontend MUST handle presentation and user interaction only. The Node.js + Express backend MUST own Jira/Confluence integrations, authorization, validation, orchestration, and business rules. PostgreSQL 15 MUST own durable project data and queryable history. Integration code MUST NOT be embedded in UI components, and database access MUST NOT be exposed directly to browsers.

### III. Contract-First Interfaces

Frontend-backend and backend-integration boundaries MUST use explicit, documented request and response contracts. Inputs MUST be validated at the boundary, errors MUST use stable machine-readable categories, and changes to shared contracts MUST include compatibility or migration notes. API behavior MUST remain deterministic for identical source data and configuration.

### IV. Secure Handling of External Systems

Credentials, tokens, and connection strings MUST come from environment variables or an approved secret manager and MUST never be committed or written to logs. Jira and Confluence permissions MUST follow least privilege. Webhook, callback, and user-supplied content MUST be authenticated, authorized, validated, and protected against replay where applicable. Sensitive data MUST be minimized in storage and responses.

### V. Reliable, Idempotent Jobs

Scheduled and on-demand automations MUST be safe to retry without duplicating pages, comments, records, or side effects. Jobs MUST define timeouts, bounded retries with backoff, rate-limit handling, and a useful failure state. Partial failures MUST be observable and MUST NOT be silently reported as successful completion.

### VI. Auditable Delivery Reporting

Every generated status report or dashboard metric MUST identify its reporting period, source scope, refresh time, and calculation assumptions. Risk, blocker, overdue, and capacity signals MUST be evidence-based. Manual overrides MUST preserve the original automated value and record who changed it, when, and why.

### VII. Testable Quality

Each feature MUST include focused automated tests for business rules, validation, error paths, and idempotency where relevant. Integration tests MUST cover external-service adapters with deterministic fixtures or approved test doubles. Frontend behavior MUST be tested at the user-visible boundary for critical workflows. A change is complete only when linting, tests, and the production build pass, or an exception is documented with owner and follow-up date.

### VIII. Containerized Reproducibility

Local development and CI MUST use the documented Docker workflow for PostgreSQL 15 and MUST avoid reliance on machine-specific services. Database schema changes MUST be versioned, reviewable, and applied through migrations. Services MUST expose health or readiness signals sufficient for dependable startup ordering and troubleshooting.

### IX. Operable by Default

Services and jobs MUST emit structured logs with correlation context, meaningful event names, and no secrets. Operational failures MUST include enough information to diagnose the affected workflow without reproducing it locally. Health checks, metrics, and alerts SHOULD focus on refresh failures, integration errors, stale data, authorization failures, and repeated retries.

## Quality Gates

Every pull request MUST demonstrate:

1. The affected user or operational outcome and the relevant source scope.
2. Updated contracts, migrations, or documentation when those interfaces change.
3. Tests covering the changed behavior and at least one relevant failure path.
4. Passing frontend and backend checks plus a production build.
5. Confirmation that secrets, personal data, and external-service permissions are handled safely.
6. Evidence that retries and reruns do not create duplicate side effects.

## Governance

This constitution is the governing standard for project decisions. When existing code conflicts with it, the change owner MUST document the conflict, its risk, and a remediation path in the pull request. Exceptions require explicit approval from a project maintainer and MUST include scope, rationale, expiration or review date, and compensating controls.

Amendments MUST be proposed as reviewed changes to this file, include an updated version and amendment date, and describe their impact on existing specifications and implementation. Principles are binding unless an approved exception exists. Feature specifications, plans, and code reviews SHOULD reference the applicable principle or quality gate when the connection is not obvious.
