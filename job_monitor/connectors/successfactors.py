import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class SuccessFactorsConnector:
    PAGE_SIZE = 25
    MAX_PAGES = 100

    def __init__(
        self,
        company_name: str,
        base_url: str,
        locations: list[str] | None = None,
        search_query: str = "intern",
    ) -> None:
        self.company_name = company_name
        self.base_url = base_url.rstrip("/") + "/"
        self.locations = locations or ["Canada", "United States"]
        self.search_query = search_query

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()

        for location in self.locations:
            for page in range(self.MAX_PAGES):
                postings = self._fetch_page(location, page * self.PAGE_SIZE)
                for job in postings:
                    if job.external_id in seen_external_ids:
                        continue
                    seen_external_ids.add(job.external_id)
                    jobs.append(job)

                if len(postings) < self.PAGE_SIZE:
                    break

        return jobs

    def _fetch_page(self, location: str, offset: int) -> list[Job]:
        response = httpx.get(
            urljoin(self.base_url, "search/"),
            params={
                "q": self.search_query,
                "locationsearch": location,
                "startrow": offset,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "Accept": "text/html",
                "User-Agent": "InternshipJobMonitor/1.0",
            },
        )
        response.raise_for_status()
        return self._parse_page(response.text)

    def _parse_page(self, html: str) -> list[Job]:
        soup = BeautifulSoup(html, "html.parser")
        jobs: list[Job] = []

        for row in soup.select("tr.data-row, div.job-row"):
            link = row.select_one(".colTitle .jobTitle-link, .jobTitle-link")
            if link is None:
                continue
            title = link.get_text(" ", strip=True)
            href = str(link.get("href") or "")
            match = re.search(r"/(\d+)/?$", href)
            if not title or not href or match is None:
                continue

            location = row.select_one(
                ".colLocation .jobLocation, "
                ".sub-section-desktop .section-field.multilocation > div"
            )
            jobs.append(
                Job(
                    external_id=match.group(1),
                    company=self.company_name,
                    title=title,
                    url=urljoin(self.base_url, href),
                    location=(
                        location.get_text(" ", strip=True)
                        if location is not None
                        else None
                    ),
                )
            )

        return jobs
