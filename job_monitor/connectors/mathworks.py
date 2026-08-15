import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class MathWorksConnector:
    BASE_URL = "https://www.mathworks.com"
    SEARCH_URL = f"{BASE_URL}/company/jobs/opportunities/search/"

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        response = httpx.get(
            self.SEARCH_URL,
            params=[
                ("display", "max"),
                ("job_type_id[]", "1755"),
                ("location[]", "US"),
                ("location[]", "CA"),
            ],
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={"User-Agent": "InternshipJobMonitor/1.0"},
        )
        response.raise_for_status()
        return self._parse_page(response.text)

    def _parse_page(self, html: str) -> list[Job]:
        soup = BeautifulSoup(html, "html.parser")
        jobs: list[Job] = []

        for link in soup.select(
            'table a[href*="/company/jobs/opportunities/"]'
        ):
            href = str(link.get("href") or "")
            id_match = re.search(r"/opportunities/(\d+)-", href)
            title = link.get_text(" ", strip=True)
            row = link.find_parent("tr")
            location_node = row.select_one(".additional_field span") if row else None
            if not id_match or not title or location_node is None:
                continue

            raw_location = location_node.get_text(" ", strip=True)
            location = self._normalize_location(raw_location)
            description_node = row.select_one(".search_highlight") if row else None
            jobs.append(
                Job(
                    external_id=id_match.group(1),
                    company=self.company_name,
                    title=title,
                    url=urljoin(self.BASE_URL, href),
                    location=location,
                    description=(
                        description_node.get_text(" ", strip=True)
                        if description_node
                        else None
                    ),
                )
            )

        return jobs

    @staticmethod
    def _normalize_location(location: str) -> str:
        parts = location.split("-", 2)
        if len(parts) == 3 and parts[0] in {"US", "CA"}:
            country = "USA" if parts[0] == "US" else "Canada"
            return f"{parts[2]}, {parts[1]}, {country}"
        return location
