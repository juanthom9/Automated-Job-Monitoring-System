from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class AmazonConnector:
    API_URL = "https://www.amazon.jobs/en/search.json"

    def __init__(
        self,
        company_name: str,
        search_query: str = "intern",
    ) -> None:
        self.company_name = company_name
        self.search_query = search_query

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        offset = 0
        limit = 100

        while True:
            response = httpx.get(
                self.API_URL,
                params={
                    "base_query": self.search_query,
                    "offset": offset,
                    "result_limit": limit,
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
            postings = data.get("jobs", [])

            for posting in postings:
                job_path = posting.get("job_path", "")
                jobs.append(
                    Job(
                        external_id=str(
                            posting.get("id_icims")
                            or posting.get("id")
                            or job_path
                        ),
                        company=self.company_name,
                        title=posting.get(
                            "title",
                            "Untitled position",
                        ),
                        url=(
                            f"https://www.amazon.jobs{job_path}"
                            if job_path.startswith("/")
                            else job_path
                        ),
                        location=(
                            posting.get("normalized_location")
                            or posting.get("location")
                        ),
                        description=posting.get("description", ""),
                    )
                )

            offset += len(postings)
            total = int(data.get("hits", 0))

            if not postings or offset >= total:
                break

        return jobs
