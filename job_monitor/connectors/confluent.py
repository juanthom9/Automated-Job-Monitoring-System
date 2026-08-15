from urllib.parse import urljoin
import time

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class ConfluentConnector:
    BASE_URL = "https://careers.confluent.io"
    JOBS_URL = f"{BASE_URL}/jobs"
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen: set[str] = set()
        page = 1

        while True:
            response = self._get_page(page)
            response.raise_for_status()
            page_jobs = self._parse_page(response.text)
            new_jobs = [job for job in page_jobs if job.external_id not in seen]
            if not new_jobs:
                break

            jobs.extend(new_jobs)
            seen.update(job.external_id for job in new_jobs)
            page += 1

        if not jobs:
            raise ValueError("Confluent careers page did not contain job rows")
        return jobs

    def _get_page(self, page: int) -> httpx.Response:
        response: httpx.Response | None = None
        for attempt in range(5):
            response = httpx.get(
                self.JOBS_URL,
                params=None if page == 1 else {"page": page},
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers=self.HEADERS,
            )
            if response.status_code != 429:
                break
            if attempt < 4:
                time.sleep(min(2**attempt, 8))

        assert response is not None
        return response

    def _parse_page(self, html: str) -> list[Job]:
        soup = BeautifulSoup(html, "html.parser")
        jobs: list[Job] = []

        for link in soup.select('a[href^="/jobs/job/"]'):
            href = str(link.get("href") or "")
            external_id = href.rstrip("/").rsplit("/", 1)[-1]
            title = link.get_text(" ", strip=True)
            row = link.find_parent(
                "div",
                class_=lambda value: value and "border-t" in value,
            )
            if not external_id or not title or row is None:
                continue

            row_parts = list(row.stripped_strings)
            locations = [
                part
                for part in row_parts
                if part not in {title, "Available in Multiple Locations"}
            ]
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=urljoin(self.BASE_URL, href),
                    location="; ".join(dict.fromkeys(locations)),
                )
            )

        return jobs
