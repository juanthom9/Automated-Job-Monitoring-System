from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class AshbyConnector:
    def __init__(
        self,
        company_name: str,
        board_name: str,
    ) -> None:
        # Save the company settings
        self.company_name = company_name
        self.board_name = board_name

    def get_api_url(self) -> str:
        # Public Ashby job board endpoint
        return (
            "https://api.ashbyhq.com/posting-api/job-board/"
            f"{self.board_name}"
        )

    def fetch_jobs(self) -> list[Job]:
        # Request all public jobs from Ashby
        response = httpx.get(
            self.get_api_url(),
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "Accept": "application/json",
                "User-Agent": "InternshipJobMonitor/1.0",
            },
        )

        response.raise_for_status()

        data: dict[str, Any] = response.json()
        postings = data.get("jobs", [])
        jobs: list[Job] = []

        for posting in postings:
            # Create one consistent Job object
            job = Job(
                external_id=str(posting.get("id", "")),
                company=self.company_name,
                title=posting.get("title", "Untitled position"),
                url=posting.get("jobUrl", ""),
                location=posting.get("location"),
                description=posting.get("descriptionPlain", ""),
            )

            jobs.append(job)

        return jobs