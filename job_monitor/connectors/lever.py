from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class LeverConnector:
    def __init__(
        self,
        company_name: str,
        site_name: str,
        region: str = "global",
    ) -> None:
        # Save the company settings
        self.company_name = company_name
        self.site_name = site_name
        self.region = region

    def get_api_url(self) -> str:
        # Lever uses a different domain for European job boards
        if self.region.lower() == "eu":
            base_url = "https://api.eu.lever.co/v0/postings"
        else:
            base_url = "https://api.lever.co/v0/postings"

        return f"{base_url}/{self.site_name}?mode=json"

    def fetch_jobs(self) -> list[Job]:
        # Request all public postings from Lever
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

        postings: list[dict[str, Any]] = response.json()
        jobs: list[Job] = []

        for posting in postings:
            # Extract the location from Lever's categories object
            categories = posting.get("categories") or {}
            location = categories.get("location")

            # Create one consistent Job object
            job = Job(
                external_id=str(posting["id"]),
                company=self.company_name,
                title=posting.get("text", "Untitled position"),
                url=posting.get("hostedUrl", ""),
                location=location,
                description=self._build_description(posting),
            )

            jobs.append(job)

        return jobs

    def _build_description(
        self,
        posting: dict[str, Any],
    ) -> str:
        # Combine useful searchable fields
        categories = posting.get("categories") or {}

        parts = [
            posting.get("descriptionPlain", ""),
            posting.get("additionalPlain", ""),
            categories.get("team", ""),
            categories.get("department", ""),
            categories.get("commitment", ""),
        ]

        return " ".join(
            str(part).strip()
            for part in parts
            if part
        )