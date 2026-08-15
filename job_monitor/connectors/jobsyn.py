from __future__ import annotations

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class JobSyncConnector:
    API_URL = "https://prod-search-api.jobsyn.org/api/v1/solr/search"

    def __init__(self, company_name: str, origin: str) -> None:
        self.company_name = company_name
        self.origin = origin

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        page = 1

        with httpx.Client(
            timeout=REQUEST_TIMEOUT_SECONDS,
            headers={
                "Accept": "application/json",
                "User-Agent": "InternshipJobMonitor/1.0",
                "X-Origin": self.origin,
            },
        ) as client:
            while True:
                response = client.get(
                    self.API_URL,
                    params={"page": page, "num_items": 10},
                )
                response.raise_for_status()
                payload = response.json()

                for item in payload.get("jobs", []):
                    guid = str(item.get("guid") or "").strip()
                    title = str(item.get("title_exact") or "").strip()
                    if not guid or not title:
                        continue

                    reqid = str(item.get("reqid") or guid).strip()
                    jobs.append(
                        Job(
                            external_id=guid,
                            company=self.company_name,
                            title=title,
                            location=str(item.get("location_exact") or "").strip(),
                            description=str(item.get("description") or ""),
                            url=(
                                "https://cgi.njoyn.com/corp/xweb/xweb.asp"
                                f"?clid=21001&lang=1&page=JobDetails&Jobid={reqid}"
                            ),
                        )
                    )

                pagination = payload.get("pagination", {})
                if not pagination.get("has_more_pages"):
                    break
                page += 1

        return jobs
