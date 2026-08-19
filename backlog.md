# Implementation Backlog: Jira Sprint Progress Dashboard

**Project Goal:** Build a Jira-based dashboard for Delivery Manager to monitor sprint health, team capacity, and risk signals for a 25-person team.

**Timeline Target:** 2-3 weeks to MVP

**Recommended Stack:** Python (backend) + Flask (lightweight web app) + Jira REST API

note which tasks now have corresponding GitHub issues (add the issue number next to each task)

---

## Phase 1: Setup & Infrastructure

### 1.1 Project Structure & Dependencies
- [ ] Create project directory structure (src/, tests/, config/, templates/, static/)
- [ ] Initialize git repository and set up .gitignore
- [ ] Create requirements.txt with core dependencies:
  - [ ] requests (Jira API calls)
  - [ ] Flask (web framework)
  - [ ] python-dotenv (environment variable management)
  - [ ] pytest (testing)
  - [ ] flask-cors (if needed for future integrations)
- [ ] Create .env.example with required environment variables (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY, JIRA_BOARD_ID)
- [ ] Create README.md with setup instructions

### 1.2 Configuration Management
- [ ] Create config.py to load environment variables
- [ ] Add validation for required environment variables
- [ ] Create a sample config for testing/development
- [ ] Document where to obtain Jira API token and board ID

### 1.3 Development Environment
- [ ] Test Jira API connectivity with sample credentials
- [ ] Verify Python version compatibility (3.8+)
- [ ] Set up local Flask development server configuration
- [ ] Create a simple health-check endpoint to verify Jira API access

---

## Phase 2: Core Features (MVP)

### 2.1 Data Layer - Enhanced (builds on data_fetcher.py)
- [ ] Extend data_fetcher.py with function to fetch active sprint ID
- [ ] Add function to retrieve all issues for active sprint with required fields
- [ ] Implement robust error handling for Jira API failures:
  - [ ] Handle rate limiting (429 response)
  - [ ] Handle authentication failures (401 response)
  - [ ] Handle network timeouts gracefully
  - [ ] Return meaningful error messages
- [ ] Add caching layer to avoid repeated API calls during testing (TTL: 5-10 minutes)
- [ ] Add logging for all API interactions

### 2.2 Data Processing Layer - Enhanced (builds on report_formatter.py)
- [ ] Refactor calculate_sprint_metrics() to include:
  - [ ] Planned vs completed story points
  - [ ] Remaining story points
  - [ ] Planned vs completed issue count
  - [ ] Completion percentage
  - [ ] Blocked issue count
  - [ ] Overdue issue count
- [ ] Create per-assignee metrics function:
  - [ ] Story points breakdown per person (planned, completed, remaining)
  - [ ] Issue count breakdown per person
  - [ ] Identify overloaded team members (define threshold)
- [ ] Add risk detection function:
  - [ ] Identify blocked issues
  - [ ] Identify overdue issues
  - [ ] Identify team members with disproportionate load
  - [ ] Flag at-risk items
- [ ] Create sprint health scoring function (Green/Yellow/Red status)

### 2.3 Dashboard UI - Basic
- [ ] Create Flask app structure (app.py, routes.py)
- [ ] Set up Jinja2 templates directory
- [ ] Create base.html template with styling (Bootstrap or simple CSS)
- [ ] Create dashboard.html with layout for:
  - [ ] Top KPI row: Sprint %, Planned vs Completed Points, Planned vs Completed Issues, Blocked Count, Overdue Count
  - [ ] Team member summary table:
    - [ ] Columns: Assignee, Planned Points, Completed Points, Remaining Points, % Complete, Issue Status
  - [ ] Risk alerts section:
    - [ ] Blocked issues list
    - [ ] Overdue items list
    - [ ] Overloaded team members alert
- [ ] Create Flask route for main dashboard (/dashboard)
- [ ] Create Flask route for JSON API (/api/sprint-data) for potential future mobile/automation use

### 2.4 Data Integration
- [ ] Create service layer to connect data fetcher → processor → dashboard
- [ ] Build dashboard controller to fetch data, process it, and pass to template
- [ ] Set up error handling for failed data retrieval (display error message on dashboard)
- [ ] Test end-to-end flow: Jira API → metrics calculation → HTML rendering

---

## Phase 3: Integration & Polish

### 3.1 Daily Refresh Capability
- [ ] Implement server-side data caching with timestamp
- [ ] Add "Last Refresh" timestamp to dashboard
- [ ] Create manual refresh button on dashboard
- [ ] (Optional for MVP) Set up APScheduler or similar for automated daily refresh
- [ ] Log all refresh events

### 3.2 UI Enhancements
- [ ] Add color coding for risk levels (Green/Yellow/Red):
  - [ ] High-risk items highlighted in red
  - [ ] Medium-risk in yellow
  - [ ] Low-risk in green
- [ ] Add hover tooltips explaining metrics
- [ ] Implement responsive design for different screen sizes
- [ ] Add progress bars for sprint completion visual
- [ ] Format currency/story points display (e.g., "25 pts")

### 3.3 Configuration & Deployment Prep
- [ ] Create production configuration separate from development
- [ ] Add security best practices:
  - [ ] Never log credentials
  - [ ] Validate user input
  - [ ] Add CSRF protection if needed
- [ ] Document environment variable requirements
- [ ] Create deployment guide (local/server options)

### 3.4 Feature Gates (for later expansion)
- [ ] Add configuration flag for trend analysis (disabled in MVP)
- [ ] Add configuration flag for multi-sprint support (disabled in MVP)
- [ ] Document how to enable features in future phases

---

## Phase 4: Testing & Quality Assurance

### 4.1 Unit Tests
- [ ] Test calculate_sprint_metrics() with various input scenarios:
  - [ ] Empty issue list
  - [ ] All issues completed
  - [ ] No issues completed
  - [ ] Mixed completion states
- [ ] Test group_issues_by_assignee() with edge cases
- [ ] Test risk detection functions with various risk scenarios
- [ ] Test health scoring logic (Green/Yellow/Red transitions)
- [ ] Aim for 80%+ code coverage on data layer

### 4.2 Integration Tests
- [ ] Test Jira API connection with real test board (or mock)
- [ ] Test end-to-end flow: API → processing → HTML output
- [ ] Test error handling:
  - [ ] Invalid Jira credentials
  - [ ] Network timeout
  - [ ] No active sprint found
  - [ ] Jira API rate limit
- [ ] Test data accuracy with known test data

### 4.3 UI/UX Testing
- [ ] Manual testing of dashboard layout on different screen sizes
- [ ] Verify all KPIs display correctly
- [ ] Verify risk alerts appear when expected
- [ ] Verify team table sorting/filtering works
- [ ] Test refresh button functionality

### 4.4 Performance Testing
- [ ] Benchmark API response time (target <10 seconds)
- [ ] Test with sprint sizes ranging from 5-50 issues
- [ ] Verify dashboard loads in <3 seconds
- [ ] Monitor memory usage

### 4.5 Security Testing
- [ ] Verify Jira credentials not exposed in logs
- [ ] Verify no secrets in version control
- [ ] Test CORS configuration (if API is exposed)
- [ ] Validate error messages don't leak sensitive info

---

## Phase 5: Documentation & Delivery

### 5.1 User Documentation
- [ ] Create User Guide explaining:
  - [ ] How to access the dashboard
  - [ ] How to interpret KPIs
  - [ ] How to read risk alerts
  - [ ] How to interpret team breakdown table
  - [ ] How to refresh data
- [ ] Create FAQ document
- [ ] Add inline help/tooltips in UI

### 5.2 Technical Documentation
- [ ] Document architecture:
  - [ ] Data flow diagram
  - [ ] Component relationships
  - [ ] API endpoints
- [ ] API documentation for /api/sprint-data endpoint (if exposed)
- [ ] Database/caching strategy (if applicable)
- [ ] Logging configuration and log locations

### 5.3 Deployment & Operations
- [ ] Create deployment guide for target environment
- [ ] Document how to set environment variables
- [ ] Create monitoring/alerting guide:
  - [ ] How to check if Jira API is accessible
  - [ ] How to debug failed data refresh
  - [ ] Common troubleshooting steps
- [ ] Create rollback procedure (if applicable)

### 5.4 Developer Documentation
- [ ] Document project structure and file organization
- [ ] Create contributor guide for future enhancements
- [ ] Document code style and conventions
- [ ] Create guide for adding new metrics/features

### 5.5 Handoff & Training
- [ ] Prepare demo/walkthrough for stakeholders
- [ ] Create quick-start guide (5-10 minutes to first data view)
- [ ] Provide credentials/access setup assistance
- [ ] Schedule training session with Delivery Manager (if needed)

---

## Nice-to-Have Features (Post-MVP)

### Phase 3+ Backlog
- [ ] **Trend Analysis:** Track sprint metrics over time (daily snapshots)
- [ ] **Historical Comparison:** Compare current sprint to previous sprints
- [ ] **Email Notifications:** Daily summary email to manager
- [ ] **Slack Integration:** Post alerts to team Slack channel
- [ ] **Custom Alert Thresholds:** Allow manager to configure risk thresholds
- [ ] **Multi-Sprint Support:** View multiple active sprints
- [ ] **Team Lead Portal:** Secondary access for team leads
- [ ] **Export to CSV/PDF:** Generate reports for stakeholders
- [ ] **Advanced Filtering:** Filter by status, issue type, custom fields

---

## Definition of Done (for MVP)

A task is considered complete when:
- [ ] Code written and reviewed
- [ ] Tests pass (80%+ coverage for data layer)
- [ ] Tested in development environment
- [ ] No console errors or warnings
- [ ] Documentation updated
- [ ] Logged as complete in backlog

---

## Sprint Planning Notes

**Recommended Sprint 1 (Week 1):**
- Phase 1: Setup & Infrastructure (1-2 days)
- Phase 2.1-2.2: Data layer enhancements (2-3 days)
- Phase 2.3-2.4: Basic dashboard UI (2-3 days)

**Recommended Sprint 2 (Weeks 2-3):**
- Phase 3: Integration & Polish (2-3 days)
- Phase 4: Testing & QA (2-3 days)
- Phase 5.1-5.3: Documentation & Deployment (1-2 days)

---

## Success Metrics for MVP

- [ ] Dashboard loads in <3 seconds
- [ ] All required KPIs display correctly
- [ ] Team breakdown table shows accurate data
- [ ] Risk alerts trigger for blocked/overdue items
- [ ] Jira API issues handled gracefully
- [ ] Data refreshes without manual intervention
- [ ] Manager can answer 5 key questions in <1 minute using dashboard
