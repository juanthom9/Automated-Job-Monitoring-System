import json
import re
from typing import Any
from urllib.parse import urljoin

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class ParadoxConnector:
    """Read public postings embedded in a Paradox careers site."""

    def __init__(
        self,
        company_name: str,
        base_url: str,
        filter_key: str | None = None,
        filter_value: str | None = None,
    ) -> None:
        self.company_name = company_name
        self.base_url = base_url.rstrip("/")
        self.filter_key = filter_key
        self.filter_value = filter_value

    def fetch_jobs(self) -> list[Job]:
        first_state = self._fetch_page(1)
        search = first_state.get("jobSearch") or {}
        total = int(search.get("totalJob") or 0)
        jobs = list(search.get("jobs") or [])

        for page in range(2, (total + 9) // 10 + 1):
            state = self._fetch_page(page)
            jobs.extend((state.get("jobSearch") or {}).get("jobs") or [])

        mapped: list[Job] = []
        seen: set[str] = set()
        for posting in jobs:
            job = self._map_job(posting)
            if job is None or job.external_id in seen:
                continue
            seen.add(job.external_id)
            mapped.append(job)
        return mapped

    def _fetch_page(self, page: int) -> dict[str, Any]:
        params = None
        if self.filter_key and self.filter_value:
            params = {f"filter[{self.filter_key}][]": self.filter_value}
        path = "/jobs" if page == 1 else f"/jobs/page/{page}"
        response = httpx.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={"User-Agent": "InternshipJobMonitor/1.0"},
        )
        response.raise_for_status()
        match = re.search(r"window\.__PRELOAD_STATE__\s*=\s*", response.text)
        if not match:
            raise ValueError("Paradox careers page did not contain job data")
        state, _ = json.JSONDecoder().raw_decode(response.text[match.end():])
        if not isinstance(state, dict):
            raise ValueError("Paradox careers job data had an unexpected shape")
        return state

    def _map_job(self, posting: dict[str, Any]) -> Job | None:
        external_id = str(
            posting.get("requisitionID") or posting.get("uniqueID") or ""
        ).strip()
        title = str(posting.get("title") or "").strip()
        relative_url = str(posting.get("originalURL") or "").strip()
        if not external_id or not title or not relative_url:
            return None

        locations = []
        for value in posting.get("locations") or []:
            location = str(
                value.get("locationParsedText")
                or value.get("locationText")
                or value.get("cityState")
                or ""
            ).strip()
            if location and location not in locations:
                locations.append(location)

        return Job(
            external_id=external_id,
            company=self.company_name,
            title=title,
            url=urljoin(f"{self.base_url}/", relative_url),
            location="; ".join(locations) or None,
        )
