from datetime import datetime
from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class OracleHCMConnector:
    # Oracle currently applies broad semantic matching even when exact search
    # is requested, so one catalog pass is sufficient before local filtering.
    SEARCH_TERMS = ("intern",)
    PAGE_SIZE = 500

    def __init__(
        self,
        company_name: str,
        api_base_url: str,
        site_number: str,
        site_path: str,
    ) -> None:
        self.company_name = company_name
        self.api_base_url = api_base_url.rstrip("/")
        self.site_number = site_number
        self.site_path = site_path.strip("/")

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()

        for search_term in self.SEARCH_TERMS:
            offset = 0
            while True:
                result = self._fetch_page(search_term, offset)
                search = (result.get("items") or [{}])[0]
                postings = search.get("requisitionList") or []

                for posting in postings:
                    job = self._map_job(posting)
                    if job is None or job.external_id in seen_external_ids:
                        continue
                    seen_external_ids.add(job.external_id)
                    jobs.append(job)

                offset += len(postings)
                total = int(search.get("TotalJobsCount") or 0)
                if not postings or offset >= total:
                    break

        return jobs

    def _fetch_page(
        self,
        search_term: str,
        offset: int,
    ) -> dict[str, Any]:
        finder = (
            f"findReqs;siteNumber={self.site_number},"
            f"limit={self.PAGE_SIZE},offset={offset},"
            f"keyword={search_term},useExactKeywordFlag=true"
        )
        response = httpx.get(
            f"{self.api_base_url}/hcmRestApi/resources/latest/"
            "recruitingCEJobRequisitions",
            params={
                "onlyData": "true",
                "expand": "requisitionList",
                "finder": finder,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "Accept": "application/json",
                "User-Agent": "InternshipJobMonitor/1.0",
            },
        )
        response.raise_for_status()
        return response.json()

    def _map_job(self, posting: dict[str, Any]) -> Job | None:
        external_id = str(posting.get("Id") or "")
        title = str(posting.get("Title") or "").strip()
        if not external_id or not title:
            return None

        posted_at = None
        if posting.get("PostedDate"):
            posted_at = datetime.fromisoformat(str(posting["PostedDate"]))

        description_parts = (
            posting.get("ShortDescriptionStr"),
            posting.get("ExternalResponsibilitiesStr"),
            posting.get("ExternalQualificationsStr"),
        )
        return Job(
            external_id=external_id,
            company=self.company_name,
            title=title,
            url=(
                f"{self.api_base_url}/hcmUI/CandidateExperience/en/sites/"
                f"{self.site_path}/job/{external_id}"
            ),
            location=posting.get("PrimaryLocation"),
            description=" ".join(
                str(value).strip()
                for value in description_parts
                if value
            ),
            posted_at=posted_at,
        )
