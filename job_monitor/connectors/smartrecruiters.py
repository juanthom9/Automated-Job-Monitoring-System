from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class SmartRecruitersConnector:
    def __init__(
        self,
        company_name: str,
        company_identifier: str,
    ) -> None:
        self.company_name = company_name
        self.company_identifier = company_identifier

    def get_api_url(self) -> str:
        return (
            "https://api.smartrecruiters.com/v1/companies/"
            f"{self.company_identifier}/postings"
        )

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        offset = 0
        limit = 100

        while True:
            response = httpx.get(
                self.get_api_url(),
                params={
                    "limit": limit,
                    "offset": offset,
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()

            data: dict[str, Any] = response.json()
            postings = data.get("content", [])

            for posting in postings:
                posting_id = str(
                    posting.get("id")
                    or posting.get("uuid")
                    or ""
                )
                location_data = posting.get("location") or {}
                location = self._format_location(location_data)

                jobs.append(
                    Job(
                        external_id=posting_id,
                        company=self.company_name,
                        title=posting.get(
                            "name",
                            "Untitled position",
                        ),
                        url=(
                            "https://jobs.smartrecruiters.com/"
                            f"{self.company_identifier}/{posting_id}"
                        ),
                        location=location,
                    )
                )

            offset += len(postings)
            total = int(data.get("totalFound", 0))

            if not postings or offset >= total:
                break

        return jobs

    @staticmethod
    def _format_location(location: dict[str, Any]) -> str | None:
        parts = [
            location.get("city"),
            location.get("region"),
            location.get("country"),
        ]
        values = [str(part) for part in parts if part]

        if location.get("remote"):
            values.append("Remote")

        return ", ".join(values) or None
