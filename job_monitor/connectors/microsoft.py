from datetime import datetime, timezone
from urllib.parse import urljoin

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class MicrosoftConnector:
    BASE_URL = "https://apply.careers.microsoft.com"
    SEARCH_URL = f"{BASE_URL}/api/pcsx/search"
    PAGE_SIZE = 10

    def __init__(
        self,
        company_name: str,
        domain: str = "microsoft.com",
        base_url: str | None = None,
    ) -> None:
        self.company_name = company_name
        self.domain = domain
        if base_url:
            self.BASE_URL = base_url.rstrip("/")
            self.SEARCH_URL = f"{self.BASE_URL}/api/pcsx/search"

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()
        start = 0

        while True:
            response = httpx.get(
                self.SEARCH_URL,
                params={
                    "domain": self.domain,
                    "query": "intern",
                    "location": "",
                    "start": start,
                    "sort_by": "relevance",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "Referer": f"{self.BASE_URL}/careers",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()
            data = response.json().get("data", {})
            postings = data.get("positions", [])

            if not postings:
                break

            for posting in postings:
                external_id = str(
                    posting.get("atsJobId")
                    or posting.get("displayJobId")
                    or posting.get("id")
                    or ""
                )
                title = str(posting.get("name") or "")
                relative_url = str(posting.get("positionUrl") or "")
                if not external_id or not title or not relative_url:
                    continue
                if external_id in seen_external_ids:
                    continue

                seen_external_ids.add(external_id)
                locations = (
                    posting.get("locations")
                    or posting.get("standardizedLocations")
                    or []
                )
                posted_timestamp = posting.get("postedTs")
                jobs.append(
                    Job(
                        external_id=external_id,
                        company=self.company_name,
                        title=title,
                        url=urljoin(self.BASE_URL, relative_url),
                        location=(
                            "; ".join(locations) if locations else None
                        ),
                        posted_at=(
                            datetime.fromtimestamp(
                                posted_timestamp,
                                tz=timezone.utc,
                            )
                            if posted_timestamp
                            else None
                        ),
                    )
                )

            start += len(postings)
            if start >= int(data.get("count", start)):
                break

        return jobs
