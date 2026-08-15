from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class TalentBrewConnector:
    def __init__(
        self,
        company_name: str,
        search_url: str,
        search_terms: list[str] | None = None,
    ) -> None:
        self.company_name = company_name
        self.search_url = search_url
        self.search_terms = search_terms or ["intern"]

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen: set[str] = set()

        for search_term in self.search_terms:
            page = 1
            while True:
                response = httpx.get(
                    self.search_url,
                    params={"k": search_term, "p": page},
                    timeout=REQUEST_TIMEOUT_SECONDS,
                    follow_redirects=True,
                    headers={"User-Agent": "InternshipJobMonitor/1.0"},
                )
                response.raise_for_status()
                page_jobs, total_pages = self._parse_page(response.text)
                for job in page_jobs:
                    if job.external_id in seen:
                        continue
                    seen.add(job.external_id)
                    jobs.append(job)

                if page >= total_pages:
                    break
                page += 1

        return jobs

    def _parse_page(self, html: str) -> tuple[list[Job], int]:
        soup = BeautifulSoup(html, "html.parser")
        results = soup.select_one('[data-selector-name="searchresults"]')
        if results is None:
            raise ValueError("TalentBrew page did not contain search results")

        total_pages = int(results.get("data-total-pages") or 1)
        jobs: list[Job] = []
        for link in results.select('a[data-job-id][href]'):
            external_id = str(link.get("data-job-id") or "")
            card = link.find_parent("li") or link.parent
            title_node = link.select_one("h2, h3") or link
            location_node = card.select_one(
                ".job-location, .location"
            )
            if not external_id or title_node is None or location_node is None:
                continue
            description_node = card.select_one(
                ".job-card__intro, .job-description"
            )
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title_node.get_text(" ", strip=True),
                    url=urljoin(self.search_url, str(link.get("href"))),
                    location=location_node.get_text(" ", strip=True),
                    description=(
                        description_node.get_text(" ", strip=True)
                        if description_node is not None
                        else ""
                    ),
                )
            )
        return jobs, total_pages
