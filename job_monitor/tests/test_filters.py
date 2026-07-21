from filters import is_relevant_job
from models import Job


def main() -> None:
    jobs = [
        Job(
            external_id="1",
            company="Example",
            title="Software Engineer Intern",
            url="https://example.com/1",
            location="Toronto, ON, Canada",
        ),
        Job(
            external_id="2",
            company="Example",
            title="Machine Learning Intern",
            url="https://example.com/2",
            location="San Francisco, CA",
        ),
        Job(
            external_id="3",
            company="Example",
            title="University Recruiter",
            url="https://example.com/3",
            location="New York, NY",
            description="Recruit software engineering interns.",
        ),
        Job(
            external_id="4",
            company="Example",
            title="Marketing Intern",
            url="https://example.com/4",
            location="Toronto, Canada",
        ),
        Job(
            external_id="5",
            company="Example",
            title="Software Engineer Intern",
            url="https://example.com/5",
            location="London, United Kingdom",
        ),
    ]

    for job in jobs:
        print(
            f"{job.title} | {job.location}: "
            f"{is_relevant_job(job)}"
        )


if __name__ == "__main__":
    main()