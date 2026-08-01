# 🔎 Automated Job Monitoring System

A configurable Python job-monitoring system that scans official career sources, filters postings, prevents duplicate alerts, and emails newly discovered matches.

The current configuration targets **computer science internships in Canada and the United States**, but the filter system can be adapted to different roles, experience levels, keywords, and locations without changing the core monitoring pipeline.

**Python · PostgreSQL · Supabase · GitHub Actions · HTTPX · Beautiful Soup · YAML**

## 👀 In One Minute

| Question | Answer |
|---|---|
| What is it? | A configurable automated pipeline for monitoring job postings from official career sources. |
| What does it do? | Collects postings, normalizes them, applies configurable filters, removes duplicates, and sends email alerts for new matches. |
| What does it currently target? | Computer science internships located in Canada or the United States. |
| Why is it interesting? | It turns many differently structured career systems into one consistent stream of job data through reusable connectors. |
| What scale does it handle? | The catalog contains 140+ configurable career sources with explicit validation and coverage tracking. |
| How does it run? | Locally on demand or automatically every 10 minutes through GitHub Actions. |

## 💡 Why I Built It

Internship searches are fragmented across many career platforms, and repeatedly checking each one is slow and error-prone. This project automates that workflow while keeping the search criteria configurable and retrieving postings from official career sources.

The current filters focus alerts on computer science internships in Canada and the United States. Because filtering is separate from collection, the system can be retargeted to other job categories or regions without rewriting its connectors or core pipeline.

## 🚀 Engineering Highlights

- **Modular source integrations:** A shared connector interface isolates platform-specific collection logic from filtering, storage, and notification code.
- **Normalized job data:** Postings from different source formats are converted into a consistent internal model before processing.
- **Persistent deduplication:** PostgreSQL records each posting by company and external job ID so the same opportunity is not emailed twice.
- **Safe first-run behavior:** The first successful scan establishes a baseline instead of treating every existing posting as new.
- **Configurable matching:** Independent keyword, role, experience-level, and location rules currently narrow results to CS internships in Canada and the United States.
- **Automated operation:** GitHub Actions runs the monitor on a recurring schedule without requiring a continuously running local machine.
- **Observable coverage:** Validation tooling reports which configured sources are working and which require investigation or a new connector.

## 🏗️ System Design

```text
Configured career sources
          |
          v
Platform and source connectors
          |
          v
Normalized job records
          |
          v
Role and location filters
          |
          v
PostgreSQL / Supabase deduplication
          |
          v
Email alerts for newly discovered matches
```

Connectors are responsible only for retrieving and parsing postings. The rest of the pipeline operates on normalized records, which makes new integrations easier to add and existing ones easier to test.

## 🛠️ Technology Stack

| Area | Technology | Purpose |
|---|---|---|
| Application | Python | Monitoring pipeline and connector framework |
| HTTP and parsing | HTTPX, Beautiful Soup | Fetching and parsing career data |
| Configuration | YAML | Source catalog and connector settings |
| Persistence | PostgreSQL, Supabase | Job history and duplicate prevention |
| Notifications | Gmail SMTP | Email alerts for new matching jobs |
| Automation | GitHub Actions | Scheduled cloud execution |
| Quality | Pytest | Connector and pipeline testing |

## ⚙️ Local Setup

1. Clone the repository and enter the project directory.

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the required credentials:

   ```env
   DATABASE_URL=postgresql://...
   EMAIL_ADDRESS=your-address@example.com
   EMAIL_APP_PASSWORD=your-app-password
   NOTIFICATION_EMAIL=destination@example.com
   ```

5. Run the monitor:

   ```powershell
   python job_monitor\monitor.py
   ```

## 📋 Source Management

The source catalog is configuration-driven. These commands help maintain and validate it:

```powershell
# Display current source coverage
python -m job_monitor.company_admin coverage

# Validate configured career sources
python -m job_monitor.company_admin validate

# List configured sources
python -m job_monitor.company_admin list
```

## 🧪 Testing

Run the automated test suite with:

```powershell
pytest
```

## ⏱️ Deployment

The included GitHub Actions workflow can run the monitor every 10 minutes. Repository secrets provide the database and email credentials used during scheduled runs. Because hosted schedulers are best-effort, an individual run may occasionally begin later than its nominal interval.

## 🔐 Responsible Access

The monitor reads publicly available job postings from official career sources. Connectors should respect each source's terms, robots guidance, and reasonable request rates. The project does not automate applications or bypass authentication, access controls, or anti-bot protections.

## 📌 Current Scope

This is a general, configurable job-monitoring system whose present use case is finding CS internships in Canada and the United States. It is also actively developed, so configured source coverage is tracked separately from successful validation as career platforms change over time.
