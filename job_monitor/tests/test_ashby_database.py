from connectors.ashby import AshbyConnector
from database import Database
from filters import is_relevant_job


def main() -> None:
    database = Database()

    # Make sure the company exists in Supabase
    company = database.add_company(
        name="Cohere",
        careers_url="https://jobs.ashbyhq.com/cohere",
        connector="ashby",
        platform_hint="Ashby",
    )

    connector = AshbyConnector(
        company_name="Cohere",
        board_name="cohere",
    )

    # Download all current Cohere jobs
    jobs = connector.fetch_jobs()

    relevant_jobs = [
        job
        for job in jobs
        if is_relevant_job(job)
    ]

    new_jobs = []

    for job in relevant_jobs:
        # Save the job only if it was not already stored
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

        if saved_job is not None:
            new_jobs.append(saved_job)

    print(f"Total jobs found: {len(jobs)}")
    print(f"Relevant internships found: {len(relevant_jobs)}")
    print(f"New jobs saved: {len(new_jobs)}")


if __name__ == "__main__":
    main()