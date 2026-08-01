import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class GoogleConnector:
    SEARCH_URL = (
        "https://www.google.com/about/careers/"
        "applications/jobs/results/"
    )
    APPLICATIONS_URL = (
        "https://www.google.com/about/careers/applications/"
    )

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()
        page = 1

        while True:
            response = httpx.get(
                self.SEARCH_URL,
                params={
                    "employment_type": "INTERN",
                    "hl": "en_US",
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
            result_cards = soup.select("div.sMn82b")

            if not result_cards:
                break

            page_jobs = 0
            for card in result_cards:
                link = card.select_one("a[href*='jobs/results/']")
                title_element = card.select_one("h3")
                location_element = card.select_one(".r0wTof")

                if not link or not title_element:
                    continue

                relative_url = str(link.get("href", ""))
                identifier_match = re.search(
                    r"jobs/results/(\d+)",
                    relative_url,
                )
                if not identifier_match:
                    continue

                external_id = identifier_match.group(1)
                if external_id in seen_external_ids:
                    continue

                seen_external_ids.add(external_id)

                jobs.append(
                    Job(
                        external_id=external_id,
                        company=self.company_name,
                        title=title_element.get_text(" ", strip=True),
                        url=urljoin(
                            self.APPLICATIONS_URL,
                            relative_url,
                        ),
                        location=(
                            location_element.get_text(" ", strip=True)
                            if location_element
                            else None
                        ),
                        description=card.get_text(" ", strip=True),
                    )
                )
                page_jobs += 1

            if page_jobs == 0:
                break

            page += 1

        return jobs
