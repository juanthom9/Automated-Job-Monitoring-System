from datetime import datetime
from typing import Any
from urllib.parse import urlencode

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class ADPWorkforceNowConnector:
    API_BASE = (
        "https://workforcenow.adp.com/mascsr/default/careercenter/"
        "public/events/staffing/v1"
    )
    CAREERS_URL = (
        "https://workforcenow.adp.com/mascsr/default/mdf/recruitment/"
        "recruitment.html"
    )

    def __init__(
        self,
        company_name: str,
        cid: str,
        cc_id: str,
        locale: str = "en_US",
    ) -> None:
        self.company_name = company_name
        self.cid = cid
        self.cc_id = cc_id
        self.locale = locale

    def fetch_jobs(self) -> list[Job]:
        response = httpx.get(
            f"{self.API_BASE}/job-requisitions",
            params={**self._params(), "$top": 1000},
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
        )
        response.raise_for_status()
        postings = response.json().get("jobRequisitions")
        if not isinstance(postings, list):
            raise ValueError("ADP careers API returned an unexpected response")

        jobs: list[Job] = []
        for posting in postings:
            external_id = self._external_id(posting)
            if not external_id:
                continue
            detail_response = httpx.get(
                f"{self.API_BASE}/job-requisitions/{external_id}",
                params=self._params(),
                headers=self._headers(),
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
            )
            detail_response.raise_for_status()
            job = self._map_job(detail_response.json(), external_id)
            if job is not None:
                jobs.append(job)
        return jobs

    def _params(self) -> dict[str, str]:
        return {
            "cid": self.cid,
            "ccId": self.cc_id,
            "lang": self.locale,
            "locale": self.locale,
        }

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "locale": self.locale,
            "User-Agent": "InternshipJobMonitor/1.0",
        }

    @staticmethod
    def _external_id(posting: dict[str, Any]) -> str:
        fields = (posting.get("customFieldGroup") or {}).get("stringFields") or []
        for field in fields:
            name = ((field.get("nameCode") or {}).get("codeValue") or "").lower()
            if name == "externaljobid":
                return str(field.get("stringValue") or "")
        return ""

    def _map_job(self, posting: dict[str, Any], external_id: str) -> Job | None:
        title = str(posting.get("requisitionTitle") or "").strip()
        if not title:
            return None

        locations = []
        for value in posting.get("requisitionLocations") or []:
            location = str((value.get("nameCode") or {}).get("shortName") or "").strip()
            if location and location not in locations:
                locations.append(location)

        posted_at = None
        if posting.get("postDate"):
            posted_at = datetime.fromisoformat(str(posting["postDate"]))

        query = urlencode(
            {
                "cid": self.cid,
                "ccId": self.cc_id,
                "lang": self.locale,
                "selectedMenuKey": "CareerCenter",
                "jobId": external_id,
            }
        )
        return Job(
            external_id=external_id,
            company=self.company_name,
            title=title,
            url=f"{self.CAREERS_URL}?{query}",
            location="; ".join(locations) or None,
            description=posting.get("requisitionDescription"),
            posted_at=posted_at,
        )
