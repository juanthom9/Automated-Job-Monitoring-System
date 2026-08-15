import json
import re
from datetime import datetime
from typing import Any

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class ShopifyConnector:
    CAREERS_URL = "https://www.shopify.com/careers"

    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        response = httpx.get(
            self.CAREERS_URL,
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "Accept": "text/html",
                "User-Agent": "InternshipJobMonitor/1.0",
            },
        )
        response.raise_for_status()
        return self._parse_page(response.text)

    def _parse_page(self, html: str) -> list[Job]:
        soup = BeautifulSoup(html, "html.parser")
        serialized = None
        for script in soup.find_all("script"):
            text = script.get_text()
            if "streamController.enqueue" in text and "jobPostingsWithJobs" in text:
                match = re.search(r"enqueue\((.*)\);\s*$", text, flags=re.DOTALL)
                if match:
                    serialized = json.loads(json.loads(match.group(1)))
                    break

        if not isinstance(serialized, list):
            raise ValueError("Shopify careers page did not contain job data")

        state = self._unflatten(serialized)
        postings = self._find_postings(state)
        if postings is None:
            raise ValueError("Shopify careers job data had an unexpected shape")

        jobs: list[Job] = []
        seen_external_ids: set[str] = set()
        for posting in postings:
            job = self._map_job(posting)
            if job is None or job.external_id in seen_external_ids:
                continue
            seen_external_ids.add(job.external_id)
            jobs.append(job)
        return jobs

    @staticmethod
    def _unflatten(values: list[Any]) -> Any:
        memo: dict[int, Any] = {}

        def resolve(reference: Any) -> Any:
            if not isinstance(reference, int):
                return reference
            if reference < 0:
                return None
            return decode(reference)

        def decode(index: int) -> Any:
            if index in memo:
                return memo[index]
            value = values[index]
            if isinstance(value, dict):
                result: dict[str, Any] = {}
                memo[index] = result
                for key, reference in value.items():
                    decoded_key = decode(int(key.removeprefix("_")))
                    result[str(decoded_key)] = resolve(reference)
                return result
            if isinstance(value, list):
                result_list: list[Any] = []
                memo[index] = result_list
                result_list.extend(resolve(item) for item in value)
                return result_list
            memo[index] = value
            return value

        return decode(0)

    @classmethod
    def _find_postings(cls, value: Any) -> list[Any] | None:
        if isinstance(value, dict):
            postings = value.get("jobPostingsWithJobs")
            if isinstance(postings, list):
                return postings
            for child in value.values():
                found = cls._find_postings(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = cls._find_postings(child)
                if found is not None:
                    return found
        return None

    def _map_job(self, value: dict[str, Any]) -> Job | None:
        posting = value.get("jobPosting") or value
        external_id = str(posting.get("id") or "")
        title = str(posting.get("title") or "").strip()
        url = str(posting.get("externalLink") or posting.get("applyLink") or "")
        if not external_id or not title or not url.startswith("https://"):
            return None

        location = str(posting.get("locationName") or "").strip()
        workplace_type = str(posting.get("workplaceType") or "").strip()
        if workplace_type and workplace_type.lower() != "onsite":
            location = f"{workplace_type} - {location}" if location else workplace_type

        posted_at = None
        if posting.get("publishedDate"):
            posted_at = datetime.fromisoformat(str(posting["publishedDate"]))

        return Job(
            external_id=external_id,
            company=self.company_name,
            title=title,
            url=url,
            location=location or None,
            posted_at=posted_at,
        )
