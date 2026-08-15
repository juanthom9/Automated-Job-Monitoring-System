from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class IntuitConnector:
    SEARCH_URL = "https://jobs.intuit.com/search-jobs"
    SEARCH_TERMS = (
        "intern",
        "internship",
        "co-op",
        "new grad",
        "student",
    )

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()

        for search_term in self.SEARCH_TERMS:
            response = httpx.get(
                self.SEARCH_URL,
                params={
                    "k": search_term,
                    "orgIds": "27595",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "text/html,application/xhtml+xml",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()

            for card in BeautifulSoup(
                response.text,
                "html.parser",
            ).select("a.sr-item[data-job-id]"):
                href = str(card.get("href") or "")
                external_id = self._external_id(card, href)
                title_element = card.select_one("h2")
                location_element = card.select_one(".job-location")

                title = (
                    title_element.get_text(" ", strip=True)
                    if title_element
                    else str(card.get("data-title") or "").strip()
                )
                if not external_id or not title or not href:
                    continue
                if external_id in seen_external_ids:
                    continue

                seen_external_ids.add(external_id)
                jobs.append(
                    Job(
                        external_id=external_id,
                        company=self.company_name,
                        title=title,
                        url=urljoin(self.SEARCH_URL, href),
                        location=(
                            location_element.get_text(" ", strip=True)
                            if location_element
                            else None
                        ),
                    )
                )

        return jobs

    @staticmethod
    def _external_id(card, href: str) -> str:
        path_id = href.rstrip("/").rsplit("/", 1)[-1]
        if path_id.isdigit():
            return path_id
        return str(card.get("data-job-id") or "")
