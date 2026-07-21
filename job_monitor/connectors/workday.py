from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class WorkdayConnector:
    def __init__(
        self,
        company_name: str,
        api_url: str,
        public_base_url: str,
    ) -> None:
        # Save the company settings
        self.company_name = company_name
        self.api_url = api_url.rstrip("/")
        self.public_base_url = public_base_url.rstrip("/")

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        offset = 0
        limit = 20

        while True:
            # Workday returns jobs in pages
            response = httpx.post(
                self.api_url,
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
                json={
                    "appliedFacets": {},
                    "limit": limit,
                    "offset": offset,
                    "searchText": "",
                },
            )

            response.raise_for_status()

            data: dict[str, Any] = response.json()
            postings = data.get("jobPostings", [])

            for posting in postings:
                external_path = posting.get("externalPath", "")
                job_url = self._build_job_url(external_path)

                # Use the requisition ID when Workday provides one
                external_id = (
                    posting.get("bulletFields", [""])[0]
                    if posting.get("bulletFields")
                    else external_path
                )

                job = Job(
                    external_id=str(external_id),
                    company=self.company_name,
                    title=posting.get(
                        "title",
                        "Untitled position",
                    ),
                    url=job_url,
                    location=posting.get("locationsText"),
                    description=" ".join(
                        str(value)
                        for value in posting.get(
                            "bulletFields",
                            [],
                        )
                    ),
                )

                jobs.append(job)

            total_jobs = data.get("total", 0)
            offset += limit

            # Stop when every page has been downloaded
            if not postings or offset >= total_jobs:
                break

        return jobs

    def _build_job_url(self, external_path: str) -> str:
        # Workday normally returns a relative job path
        if external_path.startswith("http"):
            return external_path

        return f"{self.public_base_url}{external_path}"