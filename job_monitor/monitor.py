from typing import Any

from company_loader import load_companies
from config import SEND_EXISTING_ON_FIRST_RUN
from connector_factory import create_connector
from database import Database
from emailer import EmailService
from filters import is_relevant_job


def monitor_company(
    company_config: dict[str, Any],
    database: Database,
    email_service: EmailService,
) -> None:
    company_name = company_config["name"]

    # Save or update the company in Supabase
    company = database.add_company(
        name=company_name,
        careers_url=company_config["careers_url"],
        connector=company_config["connector"],
        platform_hint=company_config.get("platform_hint"),
        enabled=company_config.get("enabled", True),
    )

    # Check whether this company completed a previous scan
    first_successful_run = not database.has_successful_check(
        company["id"]
    )

    try:
        # Create the correct connector from the YAML settings
        connector = create_connector(company_config)

        # Download all current jobs
        jobs = connector.fetch_jobs()

        # Keep only technical internships
        relevant_jobs = [
            job
            for job in jobs
            if is_relevant_job(job)
        ]

        new_jobs_count = 0
        emails_sent = 0

        for job in relevant_jobs:
            # Save the job unless it already exists
            saved_job = database.save_job(
                company_id=company["id"],
                external_id=job.external_id,
                title=job.title,
                job_url=job.url,
                location=job.location,
                description=job.description,
                posted_at=job.posted_at,
                is_relevant=True,
            )

            # None means this job was already saved
            if saved_job is None:
                continue

            new_jobs_count += 1

            # Do not email existing jobs during the first scan
            should_send_email = (
                not first_successful_run
                or SEND_EXISTING_ON_FIRST_RUN
            )

            if not should_send_email:
                continue

            try:
                # Send an alert for the new posting
                email_service.send_job_alert(job)

                database.log_email(
                    job_id=saved_job["id"],
                    recipient=email_service.recipient,
                    status="sent",
                )

                emails_sent += 1

            except Exception as email_error:
                # Record failed email attempts
                database.log_email(
                    job_id=saved_job["id"],
                    recipient=email_service.recipient,
                    status="failed",
                    error_message=str(email_error),
                )

                print(
                    f"{company_name}: email failed for "
                    f"{job.title}: {email_error}"
                )

        # Record the completed company scan
        database.log_monitor_result(
            company_id=company["id"],
            status="success",
            jobs_found=len(jobs),
            relevant_jobs_found=len(relevant_jobs),
        )

        print(f"\n{company_name}")
        print(f"Total jobs: {len(jobs)}")
        print(f"Relevant internships: {len(relevant_jobs)}")
        print(f"New jobs saved: {new_jobs_count}")
        print(f"Emails sent: {emails_sent}")

        if first_successful_run:
            print("Initial baseline completed.")

    except Exception as error:
        # Record the failed company scan
        database.log_monitor_result(
            company_id=company["id"],
            status="failed",
            error_message=str(error),
        )

        print(f"\n{company_name} failed: {error}")


def main() -> None:
    database = Database()
    email_service = EmailService()

    # Ensure all required tables exist
    database.create_tables()

    # Load every enabled company
    companies = load_companies()

    print(f"Monitoring {len(companies)} companies...")

    for company in companies:
        monitor_company(
            company_config=company,
            database=database,
            email_service=email_service,
        )

    print("\nMonitoring run completed.")


if __name__ == "__main__":
    main()