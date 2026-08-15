from typing import Any
import re

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class WorkdayConnector:
    def __init__(
        self,
        company_name: str,
        api_url: str,
        public_base_url: str,
        search_terms: list[str] | None = None,
        additional_sites: list[dict[str, str]] | None = None,
    ) -> None:
        # Save the company settings
        self.company_name = company_name
        self.api_url = api_url.rstrip("/")
        self.public_base_url = public_base_url.rstrip("/")
        self.search_terms = search_terms or [""]
        self.sites = [
            {"api_url": self.api_url, "public_base_url": self.public_base_url},
            *(additional_sites or []),
        ]

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()

        for site in self.sites:
            for search_term in self.search_terms:
                self._fetch_search(
                    search_term,
                    jobs,
                    seen_external_ids,
                    site["api_url"].rstrip("/"),
                    site["public_base_url"].rstrip("/"),
                )

        return jobs

    def _fetch_search(
        self,
        search_term: str,
        jobs: list[Job],
        seen_external_ids: set[str],
        api_url: str,
        public_base_url: str,
    ) -> None:
        offset = 0
        limit = 20

        while True:
            # Workday returns jobs in pages
            response = httpx.post(
                api_url,
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
                json={
                    "appliedFacets": {},
                    "limit": limit,
                    "offset": offset,
                    "searchText": search_term,
                },
            )

            response.raise_for_status()

            data: dict[str, Any] = response.json()
            postings = data.get("jobPostings", [])

            for posting in postings:
                external_path = posting.get("externalPath", "")
                job_url = self._build_job_url(external_path, public_base_url)
                location = posting.get("locationsText")
                description = " ".join(
                    str(value)
                    for value in posting.get("bulletFields", [])
                )

                if location and re.fullmatch(
                    r"\d+ Locations?",
                    location,
                    flags=re.IGNORECASE,
                ):
                    detail = self._fetch_job_detail(external_path, api_url)
                    detail_info = detail.get("jobPostingInfo", {})
                    detail_locations = [
                        detail_info.get("location"),
                        *(detail_info.get("additionalLocations") or []),
                    ]
                    location = "; ".join(
                        str(value)
                        for value in detail_locations
                        if value
                    ) or location
                    detail_description = detail_info.get("jobDescription")
                    if detail_description:
                        description = BeautifulSoup(
                            str(detail_description),
                            "html.parser",
                        ).get_text(" ", strip=True)

                # Use the requisition ID when Workday provides one
                external_id = (
                    posting.get("bulletFields", [""])[0]
                    if posting.get("bulletFields")
                    else external_path
                )

                external_id = str(external_id)

                if external_id in seen_external_ids:
                    continue

                seen_external_ids.add(external_id)

                job = Job(
                    external_id=external_id,
                    company=self.company_name,
                    title=posting.get(
                        "title",
                        "Untitled position",
                    ),
                    url=job_url,
                    location=location,
                    description=description,
                )

                jobs.append(job)

            total_jobs = data.get("total", 0)
            offset += limit

            # Stop when every page has been downloaded
            if not postings or offset >= total_jobs:
                break

    def _build_job_url(
        self,
        external_path: str,
        public_base_url: str | None = None,
    ) -> str:
        # Workday normally returns a relative job path
        if external_path.startswith("http"):
            return external_path

        return f"{public_base_url or self.public_base_url}{external_path}"

    def _fetch_job_detail(
        self,
        external_path: str,
        api_url: str | None = None,
    ) -> dict[str, Any]:
        response = httpx.get(
            f"{(api_url or self.api_url).removesuffix('/jobs')}{external_path}",
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "Accept": "application/json",
                "User-Agent": "InternshipJobMonitor/1.0",
            },
        )
        response.raise_for_status()
        return response.json()
