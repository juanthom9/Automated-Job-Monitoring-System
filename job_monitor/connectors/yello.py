from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class YelloConnector:
    PAGE_SIZE = 25
    MAX_PAGES = 100

    def __init__(
        self,
        company_name: str,
        board_id: str,
        country_filter_ids: list[int],
        search_query: str = "intern",
    ) -> None:
        self.company_name = company_name
        self.board_id = board_id
        self.country_filter_ids = country_filter_ids
        self.search_query = search_query
        self.base_url = "https://eyglobal.yello.co/"

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen: set[str] = set()

        for page in range(1, self.MAX_PAGES + 1):
            response = httpx.get(
                urljoin(self.base_url, f"job_boards/{self.board_id}/search"),
                params={
                    "query": self.search_query,
                    "filters": ",".join(map(str, self.country_filter_ids)),
                    "page_number": page,
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()
            data = response.json()
            postings = self._parse_results(str(data.get("html") or ""))
            for job in postings:
                if job.external_id in seen:
                    continue
                seen.add(job.external_id)
                jobs.append(job)
            if not data.get("more_requisitions"):
                break

        return jobs

    def _parse_results(self, html: str) -> list[Job]:
        soup = BeautifulSoup(html, "html.parser")
        jobs: list[Job] = []
        for item in soup.select("li.search-results__item"):
            link = item.select_one("a.search-results__req_title")
            requisition = item.select_one(".search-results__jobinfo div span")
            if link is None or requisition is None:
                continue
            title = link.get_text(" ", strip=True)
            external_id = requisition.get_text(" ", strip=True)
            href = str(link.get("href") or "")
            if not title or not external_id or not href:
                continue
            location = (
                "Canada"
                if "canada" in title.lower()
                else "Canada or United States"
            )
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=urljoin(self.base_url, href),
                    location=location,
                )
            )
        return jobs
