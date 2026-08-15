import json
from typing import Any

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class PlaidConnector:
    CAREERS_URL = "https://plaid.com/careers/"

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        response = httpx.get(
            self.CAREERS_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={"User-Agent": "InternshipJobMonitor/1.0"},
        )
        response.raise_for_status()
        return self._parse_page(response.text)

    def _parse_page(self, html: str) -> list[Job]:
        soup = BeautifulSoup(html, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if script is None or not script.string:
            raise ValueError("Plaid careers page did not contain job data")
        page_props = json.loads(script.string)["props"]["pageProps"]
        postings = self._find_jobs(page_props)
        if postings is None:
            raise ValueError("Plaid careers job data had an unexpected shape")

        jobs: list[Job] = []
        for posting in postings:
            external_id = str(posting.get("id") or "").strip()
            title = str(posting.get("title") or "").strip()
            key = str(posting.get("key") or "").strip().strip("/")
            if not external_id or not title or not key:
                continue
            locations = [str(value) for value in posting.get("locations") or []]
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=f"{self.CAREERS_URL}openings/{key}/",
                    location="; ".join(locations) or None,
                    description=str(posting.get("department") or ""),
                )
            )
        return jobs

    @classmethod
    def _find_jobs(cls, value: Any) -> list[dict[str, Any]] | None:
        if isinstance(value, dict):
            jobs = value.get("jobsData")
            if isinstance(jobs, list):
                return jobs
            for child in value.values():
                found = cls._find_jobs(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = cls._find_jobs(child)
                if found is not None:
                    return found
        return None
