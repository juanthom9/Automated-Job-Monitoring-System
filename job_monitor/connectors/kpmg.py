from dataclasses import replace
from urllib.parse import parse_qs, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from connectors.jibe import JibeConnector
from models import Job


class KPMGConnector:
    US_SEARCH_URL = "https://www.kpmguscareers.com/job-search/"

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        canada = JibeConnector(
            self.company_name,
            "https://careers.kpmg.ca/api/jobs",
            "https://careers.kpmg.ca/job",
            include_description=False,
        ).fetch_jobs()
        return [
            *(replace(job, external_id=f"ca:{job.external_id}") for job in canada),
            *(replace(job, external_id=f"us:{job.external_id}") for job in self._fetch_us()),
        ]

    def _fetch_us(self) -> list[Job]:
        response = httpx.get(
            self.US_SEARCH_URL,
            params={"career-level": "Internship|", "spage": 1},
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={"User-Agent": "InternshipJobMonitor/1.0"},
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jobs: list[Job] = []
        for card in soup.select(".search--item"):
            link = card.select_one('a[href*="jobId="]')
            title_element = card.select_one(".h4")
            if link is None or title_element is None:
                continue
            href = str(link.get("href") or "")
            external_id = parse_qs(urlparse(href).query).get("jobId", [""])[0]
            title = title_element.get_text(" ", strip=True)
            if not external_id or not title:
                continue
            jobs.append(
                Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=title,
                    url=urljoin(self.US_SEARCH_URL, href),
                    location="United States",
                )
            )
        return jobs
