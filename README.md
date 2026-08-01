# Automated Job Monitoring System

A Python service that monitors official company career sources for computer-science-related internships and early-career roles in Canada and the United States.

The monitor collects postings through modular applicant-tracking-system connectors, applies configurable title and location filters, stores discovered jobs in PostgreSQL, and sends an email when a new matching position appears. It is designed to run automatically through GitHub Actions while avoiding duplicate notifications between runs.

## Features

- Monitors a YAML-configured catalog of company career sources.
- Uses reusable connectors for shared applicant tracking systems and dedicated connectors where necessary.
- Filters for software engineering, data, machine learning, infrastructure, security, research, and related early-career roles.
- Limits results to Canada and the United States.
- Excludes senior, leadership, sales, marketing, product-management, and other non-target positions.
- Stores jobs and monitoring history in PostgreSQL or Supabase.
- Prevents duplicate alerts with a persistent company and external-job-ID constraint.
- Establishes a silent baseline on the first successful run so existing postings do not flood the inbox.
- Sends HTML and plain-text alerts through Gmail SMTP.
- Supports scheduled and manually triggered GitHub Actions runs.
- Generates a coverage report distinguishing validated, unresolved, and unsupported sources.

## How it works

```text
Configured career sources
        -> ATS connectors
        -> normalized job records
        -> role and location filters
        -> PostgreSQL deduplication
        -> email alert for each new match
```

Each connector converts its source into the same internal job model. This keeps filtering, persistence, and notification logic independent of the underlying hiring platform.

## Technology

- Python
- HTTPX and Beautiful Soup
- PostgreSQL / Supabase
- Gmail SMTP
- GitHub Actions
- YAML configuration

## Local setup

Create and activate a virtual environment from the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Configure the following values:

```env
DATABASE_URL=your_postgresql_connection_string
SMTP_EMAIL=your_gmail_address
SMTP_PASSWORD=your_gmail_app_password
ALERT_EMAIL=notification_recipient
SEND_EXISTING_ON_FIRST_RUN=false
REQUEST_TIMEOUT_SECONDS=30
```

Use a Gmail app password rather than your normal account password. Do not commit `.env`.

## Run the monitor

```powershell
python job_monitor\monitor.py
```

Database tables are created automatically. By default, the first successful scan records matching jobs without sending alerts. Subsequent runs notify only for newly discovered matches.

## Manage sources

List configured sources:

```powershell
python job_monitor\manage.py list-companies
```

Add or update a source:

```powershell
python job_monitor\manage.py add-company --name "Example" --url "https://example.com/careers"
```

Generate the coverage report:

```powershell
python job_monitor\manage.py coverage-report
```

Configuration lives in `job_monitor/companies.yaml`. A configured source is not assumed to work until its connector has been validated against the live career system.

## Filtering

Filtering rules are defined in `job_monitor/filters.py`. A posting must:

1. Identify an internship, co-op, student, new-graduate, or college-graduate role.
2. Match a targeted technical field in its title or description.
3. Have a supported Canadian or US location.
4. Avoid excluded non-technical and senior title patterns.

The rules are intentionally configurable rather than tied to one degree program or hiring season.

## Tests

Install the test runner and execute the suite from the repository root:

```powershell
pip install pytest
pytest job_monitor\tests
```

## Automation

The included GitHub Actions workflow can run manually or on its configured schedule. Add these repository secrets before enabling scheduled monitoring:

- `DATABASE_URL`
- `SMTP_EMAIL`
- `SMTP_PASSWORD`
- `ALERT_EMAIL`

Scheduled GitHub Actions runs are best-effort and may start later than the requested cron interval during periods of high demand.

## Responsible access

The project uses official public career pages and supported public job-board interfaces. Sources that prohibit automation, require permission, or actively block automated access remain disabled until an approved integration is available. The monitor does not submit job applications or bypass access controls.
