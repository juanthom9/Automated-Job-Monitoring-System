from connectors.ashby import AshbyConnector
from filters import is_relevant_job


def main() -> None:
    # Cohere uses an Ashby board
    connector = AshbyConnector(
        company_name="Cohere",
        board_name="cohere",
    )

    # Download all public Cohere jobs
    jobs = connector.fetch_jobs()

    print(f"Total jobs found: {len(jobs)}")

    relevant_jobs = [
        job
        for job in jobs
        if is_relevant_job(job)
    ]

    print(
        f"Relevant internships found: "
        f"{len(relevant_jobs)}"
    )

    for job in relevant_jobs:
        print()
        print(job.title)
        print(job.location)
        print(job.url)


if __name__ == "__main__":
    main()