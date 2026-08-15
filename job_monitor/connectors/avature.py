import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class AvatureConnector:
    PAGE_SIZE = 20
    MAX_PAGES = 100

    def __init__(
        self,
        company_name: str,
        search_url: str,
        page_size: int | None = None,
    ) -> None:
        self.company_name = company_name
        self.search_url = search_url
        self.page_size = page_size or self.PAGE_SIZE

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen: set[str] = set()

        for page in range(self.MAX_PAGES):
            postings = self._fetch_page(page * self.page_size)
            for job in postings:
                if job.external_id in seen:
                    continue
                seen.add(job.external_id)
                jobs.append(job)
            if len(postings) < self.page_size:
                break

        return jobs

    def _fetch_page(self, offset: int) -> list[Job]:
        response = httpx.get(
            self.search_url,
            params={
                "jobRecordsPerPage": self.page_size,
                "jobOffset": offset,
            },
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

        for link in soup.select('a[href*="/JobDetail/"]'):
            href = str(link.get("href") or "")
            match = re.search(r"/(\d+)/?$", href)
            row = link.find_parent("tr")
            article = link.find_parent("article")
            if match is None or (row is None and article is None):
                continue
            external_id = match.group(1)
            if external_id in seen:
                continue
            seen.add(external_id)
            title = link.get_text(" ", strip=True)
            if row is not None:
                cells = row.find_all("td")
                location = cells[0].get_text(" ", strip=True) if cells else None
            else:
                location_element = article.select_one(".list-item-location")
                if location_element is None:
                    subtitle = article.select_one(".article__header__text__subtitle")
                    subtitle_spans = subtitle.find_all("span") if subtitle else []
                    location_element = subtitle_spans[-1] if subtitle_spans else None
                location = (
                    location_element.get_text(" ", strip=True)
                    if location_element is not None
                    else None
                )
            if not title:
                continue
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=urljoin(self.search_url, href),
                    location=location or None,
                )
            )

        return jobs
