from datetime import datetime
from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class JibeConnector:
    PAGE_SIZE = 100
    MAX_PAGES = 100

    def __init__(
        self,
        company_name: str,
        api_url: str,
        public_job_base_url: str,
        include_description: bool = True,
    ) -> None:
        self.company_name = company_name
        self.api_url = api_url
        self.public_job_base_url = public_job_base_url.rstrip("/")
        self.include_description = include_description

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()

        for page in range(1, self.MAX_PAGES + 1):
            response = httpx.get(
                self.api_url,
                params={"page": page, "limit": self.PAGE_SIZE},
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            postings = result.get("jobs")
            if not isinstance(postings, list):
                raise ValueError("Jibe careers API returned an unexpected response")

            for posting in postings:
                job = self._map_job(posting)
                if job is None or job.external_id in seen_external_ids:
                    continue
                seen_external_ids.add(job.external_id)
                jobs.append(job)

            total = int(result.get("totalCount") or result.get("count") or 0)
            if not postings or len(jobs) >= total or len(postings) < self.PAGE_SIZE:
                break

        return jobs

    def _map_job(self, posting: dict[str, Any]) -> Job | None:
        data = posting.get("data") or posting
        external_id = str(data.get("req_id") or data.get("slug") or "")
        title = str(data.get("title") or "").strip()
        if not external_id or not title:
            return None

        posted_at = None
        if data.get("posted_date"):
            posted_at = datetime.fromisoformat(
                str(data["posted_date"]).replace("Z", "+00:00")
            )

        description_parts = (
            data.get("description"),
            data.get("responsibilities"),
            data.get("qualifications"),
        )
        language = str(data.get("language") or "en-us")
        return Job(
            external_id=external_id,
            company=self.company_name,
            title=title,
            url=f"{self.public_job_base_url}/{external_id}?lang={language}",
            location=(
                data.get("full_location")
                or data.get("location_name")
                or data.get("country")
            ),
            description=(
                " ".join(str(value) for value in description_parts if value)
                if self.include_description
                else None
            ),
            posted_at=posted_at,
        )
