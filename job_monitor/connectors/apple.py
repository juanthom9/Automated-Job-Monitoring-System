from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class AppleConnector:
    SEARCH_URL = "https://jobs.apple.com/en-ca/search"

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        page = 1

        while True:
            response = httpx.get(
                self.SEARCH_URL,
                params={
                    "team": "internships-STDNT-INTRN",
                    "page": page,
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "text/html,application/xhtml+xml",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            result_cards = soup.select(
                "div.job-title.job-list-item"
            )

            if not result_cards:
                break

            for card in result_cards:
                link = card.select_one("h3 a[href*='/details/']")
                location_element = card.select_one(
                    ".job-title-location span:not(.a11y)"
                )

                if not link or not link.get("href"):
                    continue

                relative_url = str(link["href"])
                path_parts = [
                    part
                    for part in urlparse(relative_url).path.split("/")
                    if part
                ]
                external_id = (
                    path_parts[path_parts.index("details") + 1]
                    if "details" in path_parts
                    else relative_url
                )

                jobs.append(
                    Job(
                        external_id=external_id,
                        company=self.company_name,
                        title=link.get_text(" ", strip=True),
                        url=urljoin(self.SEARCH_URL, relative_url),
                        location=(
                            location_element.get_text(" ", strip=True)
                            if location_element
                            else None
                        ),
                    )
                )

            page += 1

        return jobs
