from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class PhenomConnector:
    def __init__(
        self,
        company_name: str,
        api_url: str,
        query_params: dict[str, Any] | None = None,
    ) -> None:
        self.company_name = company_name
        self.api_url = api_url
        self.query_params = query_params or {}

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        offset = 0
        limit = 100

        while True:
            params = {
                **self.query_params,
                "limit": limit,
                "offset": offset,
            }
            response = httpx.get(
                self.api_url,
                params=params,
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

            for posting in postings:
                job_data = posting.get("data") or posting
                metadata = job_data.get("meta_data") or {}
                canonical_url = metadata.get("canonical_url")

                jobs.append(
                    Job(
                        external_id=str(
                            job_data.get("req_id")
                            or job_data.get("slug")
                            or ""
                        ),
                        company=self.company_name,
                        title=job_data.get(
                            "title",
                            "Untitled position",
                        ),
                        url=(
                            canonical_url
                            or job_data.get("apply_url", "")
                        ),
                        location=(
                            job_data.get("full_location")
                            or job_data.get("location_name")
                        ),
                        description=job_data.get("description", ""),
                    )
                )

            offset += len(postings)
            total = int(
                data.get("totalCount")
                or data.get("count")
                or 0
            )

            if not postings or offset >= total:
                break

        return jobs
