- **Purpose:** Implement Phase 1 setup/infrastructure and Phase 2 core MVP features for the Jira sprint progress dashboard.
- **Input format:** Accept a task request containing the target phase or backlog item, existing files to extend, expected behavior, and available Jira/test configuration.
  + Use Python 3.8+ source files, Markdown documentation, JSON configuration, and Jira issue payloads as applicable.
  + Represent Jira issue input as a list of objects with `key` and `fields`; include `summary`, `status`, `assignee`, `storyPoints`, `duedate`, labels, and sprint data when available.
  + Never require real credentials for local tests; use environment variables or mocks for Jira access.
- **Processing steps:**
  + Read `./backlog.md`, the relevant existing module, and nearby tests before editing.
  + Map each requested change to a Phase 1 or Phase 2 backlog item and keep the change within that scope.
  + For Phase 1, create or update the project structure, dependencies, environment template, configuration validation, README setup steps, Jira connectivity check, and health-check endpoint.
  + For Phase 2 data work, fetch the active sprint and issue fields, handle HTTP 401/429 errors and timeouts, cache responses for 5–10 minutes where appropriate, and log requests without secrets.
  + For Phase 2 processing, calculate planned/completed/remaining points and issues, completion percentage, blocked and overdue counts, per-assignee load, risk flags, and Green/Yellow/Red sprint health.
  + For Phase 2 UI and integration, connect fetcher → processor → Flask routes/templates, expose `/dashboard` and `/api/sprint-data`, and render KPI, team, and risk sections.
  + Add or update focused tests for empty, complete, incomplete, mixed, blocked, overdue, API-error, and unassigned-issue cases.
  + Run the narrowest relevant test, type, lint, or syntax check after each substantive edit; update backlog checkboxes only for verified work.
- **Output format:** Return or write implementation artifacts in their established project locations and summarize completed backlog items, tests run, and unresolved dependencies.
  + API functions should return structured Python data or raise clear, typed errors; do not return credential values.
  + Dashboard JSON should include sprint metrics, assignee metrics, risk items, health status, and refresh/error metadata.
  + Documentation should include setup commands, required environment variables, endpoint paths, and expected error behavior.
- **Constraints:**
  + Keep the MVP limited to one active sprint, Jira as the source, daily-refresh-ready behavior, and a 25-person team view.
  + Do not commit `.env` files, API tokens, passwords, or secrets; preserve `.env.example` as placeholders only.
  + Keep Jira access separate from metric calculation and dashboard rendering.
  + Preserve existing public APIs unless the backlog item requires a compatible extension.
  + Do not claim a backlog item complete without executable validation; record unavailable credentials or external dependencies as blockers.
  + Meet the project targets of under 10 seconds for standard sprint queries and under 3 seconds for dashboard loading where measurable.