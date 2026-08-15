from urllib.parse import parse_qs, urlparse

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class ValveConnector:
    CAREERS_URL = "https://www.valvesoftware.com/en/jobs"

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
        jobs: list[Job] = []
        seen: set[str] = set()

        for link in soup.select('a[href*="/jobs?job_id="]'):
            url = str(link.get("href") or "")
            external_id = parse_qs(urlparse(url).query).get("job_id", [""])[0]
            title = link.get_text(" ", strip=True)
            if not external_id or not title or external_id in seen:
                continue
            seen.add(external_id)
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=url,
                    location="Bellevue, WA, USA",
                )
            )

        if not jobs:
            raise ValueError("Valve careers page did not contain job links")
        return jobs
