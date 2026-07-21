# Automatic Internship Job Monitor

A backend-only Python service that checks official company career pages, discovers common applicant-tracking systems, filters for technical internships/co-ops, stores seen jobs in PostgreSQL, and emails each newly detected match.

The supplied `companies.yaml` contains 144 official career-board URLs. The first successful check for a company creates a baseline and does **not** email existing jobs. Future newly discovered jobs are emailed once.

## What “automatic discovery” means

The detector follows redirects and inspects the career page for links or embedded URLs belonging to:

- Greenhouse
- Lever
- Ashby
- Workday

Direct platform URLs are recognized immediately. If no supported platform is found, the monitor uses a basic HTML fallback and logs a low-confidence result. Proprietary/JavaScript-heavy boards such as Google Careers, Microsoft Careers, Amazon Jobs, Apple Jobs, and some Phenom/SuccessFactors sites can require dedicated connectors later; automatic detection cannot turn every custom site into a reliable API.

## 1. Open in VS Code

Extract the project, then open the `job-monitor` folder in VS Code.

## 2. Create the Python environment (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Select it with `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv`.

## 3. Configure Supabase and Resend

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Fill in:

```env
DATABASE_URL=your_supabase_session_pooler_connection_string
RESEND_API_KEY=re_your_key
ALERT_EMAIL=your_email@example.com
FROM_EMAIL=Job Monitor <alerts@your_verified_domain.com>
SEND_EXISTING_ON_FIRST_RUN=false
REQUEST_TIMEOUT_SECONDS=30
```

The program creates its database tables automatically. Never commit `.env`.

## 4. Discover the platforms before deployment

Run this locally:

```powershell
python manage.py discover-all
```

This inspects every supplied URL and writes the detected connector/settings into `companies.yaml`. Review the output. `high` confidence generally means a supported ATS was identified; `low` means the generic HTML fallback will be used.

Run it again whenever a company changes its careers platform.

## 5. Add a company later

You only need its name and official careers/job-board URL:

```powershell
python manage.py add-company --name "Example Company" --url "https://example.com/careers"
```

An optional hint can be supplied:

```powershell
python manage.py add-company --name "Example Company" --url "https://example.com/careers" --platform "Greenhouse"
```

The command discovers the connector and adds or updates the company in `companies.yaml` with `enabled: true`.

To disable a company, open `companies.yaml` and change:

```yaml
enabled: false
```

## 6. Test locally

```powershell
python main.py
```

The first run records current matching roles as a baseline. Run it again to confirm there are no duplicate emails.

Run tests:

```powershell
pip install pytest
pytest
```

## 7. Keyword filtering

Edit `job_monitor/filters.py`. A job must match both:

1. an internship/student pattern (`intern`, `internship`, `co-op`, etc.), and
2. a technical pattern (`software`, `developer`, `machine learning`, `data`, `security`, etc.).

Senior and leadership titles are excluded.

## 8. Deploy with GitHub Actions

Create an empty GitHub repository and push the folder:

```powershell
git init
git add .
git commit -m "Build automatic internship monitor"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Add these GitHub Actions secrets under **Settings → Secrets and variables → Actions**:

- `DATABASE_URL`
- `RESEND_API_KEY`
- `ALERT_EMAIL`
- `FROM_EMAIL`

The included workflow requests a run every ten minutes. GitHub schedules may occasionally be delayed.

## Recommended rollout

Do not trust all 144 sites immediately. First run `discover-all`, then enable/test supported high-confidence platforms in batches. Review GitHub Action logs for zero-job results or repeated errors. Custom career systems should receive dedicated connectors rather than relying indefinitely on generic HTML parsing.
