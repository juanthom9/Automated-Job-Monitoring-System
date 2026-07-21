from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class GreenhouseConnector:
    def __init__(
        self,
        company_name: str,
        board_token: str,
    ) -> None:
        # Save the company settings
        self.company_name = company_name
        self.board_token = board_token

    def get_api_url(self) -> str:
        # Public Greenhouse job board endpoint
        return (
            "https://boards-api.greenhouse.io/v1/boards/"
            f"{self.board_token}/jobs?content=true"
        )

    def fetch_jobs(self) -> list[Job]:
        # Request all published Greenhouse jobs
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
            location_data = posting.get("location") or {}
            location = location_data.get("name")

            # Convert every posting to the shared Job model
            job = Job(
                external_id=str(posting.get("id", "")),
                company=self.company_name,
                title=posting.get("title", "Untitled position"),
                url=posting.get("absolute_url", ""),
                location=location,
                description=posting.get("content", ""),
            )

            jobs.append(job)

        return jobs