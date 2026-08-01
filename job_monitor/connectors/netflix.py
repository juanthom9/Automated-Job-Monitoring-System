import html
import json

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class NetflixConnector:
    SEARCH_URL = "https://explore.jobs.netflix.net/careers"

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        response = httpx.get(
            self.SEARCH_URL,
            params={
                "domain": "netflix.com",
                "query": "intern",
                "sort_by": "relevance",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "Accept": "text/html,application/xhtml+xml",
                "User-Agent": "InternshipJobMonitor/1.0",
            },
        )
        response.raise_for_status()

        data_element = BeautifulSoup(
            response.text,
            "html.parser",
        ).select_one("#smartApplyData")
        if data_element is None:
            raise ValueError(
                "Netflix careers page did not contain smartApplyData"
            )

        payload = json.loads(
            html.unescape(data_element.get_text(strip=True))
        )
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()

        for posting in payload.get("positions", []):
            external_id = str(
                posting.get("ats_job_id") or posting.get("id") or ""
            )
            title = str(posting.get("name") or "")
            url = str(posting.get("canonicalPositionUrl") or "")
            if not external_id or not title or not url:
                continue
            if external_id in seen_external_ids:
                continue

            seen_external_ids.add(external_id)
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=url,
                    location=posting.get("location"),
                    description=posting.get("job_description"),
                )
            )

        return jobs
