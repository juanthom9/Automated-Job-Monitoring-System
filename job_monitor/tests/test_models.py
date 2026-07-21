from models import Job


def main() -> None:
    # Create a sample job
    job = Job(
        external_id="wealthsimple-123",
        company="Wealthsimple",
        title="Software Engineer Intern",
        url="https://jobs.lever.co/wealthsimple/example-job",
        location="Toronto, Canada",
    )

    # Display the job values
    print(job)
    print(job.title)
    print(job.location)


if __name__ == "__main__":
    main()