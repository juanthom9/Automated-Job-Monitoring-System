from connectors.lever import LeverConnector
from filters import is_relevant_job


def main() -> None:
    # Wealthsimple's Lever site name
    connector = LeverConnector(
        company_name="Wealthsimple",
        site_name="wealthsimple",
    )

    # Download all public Wealthsimple jobs
    jobs = connector.fetch_jobs()

    print(f"Total jobs found: {len(jobs)}")

    # Keep only relevant technical student roles
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