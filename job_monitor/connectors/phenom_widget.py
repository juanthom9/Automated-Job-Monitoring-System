from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class PhenomWidgetConnector:
    def __init__(
        self,
        company_name: str,
        widget_url: str,
        ref_num: str,
        locale: str = "en_global",
        country: str = "global",
        search_term: str = "intern",
        job_url_template: str | None = None,
        company_names: list[str] | None = None,
        content_terms: list[str] | None = None,
    ) -> None:
        self.company_name = company_name
        self.widget_url = widget_url
        self.ref_num = ref_num
        self.locale = locale
        self.country = country
        self.search_term = search_term
        self.job_url_template = job_url_template
        self.company_names = {
            name.casefold() for name in (company_names or [])
        }
        self.content_terms = [
            term.casefold() for term in (content_terms or [])
        ]

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()
        offset = 0
        page_size = 100

        while True:
            response = httpx.post(
                self.widget_url,
                json={
                    "ddoKey": "refineSearch",
                    "pageSize": page_size,
                    "from": offset,
                    "size": page_size,
                    "siteType": "external",
                    "keywords": self.search_term,
                    "locale": self.locale,
                    "country": self.country,
                    "deviceType": "desktop",
                    "refNum": self.ref_num,
                    "sortBy": "Most relevant",
                    "jobs": True,
                    "counts": True,
                    "getFilters": False,
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()
            search: dict[str, Any] = response.json().get(
                "refineSearch",
                {},
            )
            postings = (search.get("data") or {}).get("jobs") or []

            for posting in postings:
                posting_company = str(
                    posting.get("companyName") or ""
                ).casefold()
                if (
                    self.company_names
                    and posting_company not in self.company_names
                ):
                    continue
                searchable_text = " ".join(
                    str(posting.get(key) or "")
                    for key in (
                        "title",
                        "description",
                        "descriptionTeaser",
                    )
                ).casefold()
                if self.content_terms and not any(
                    term in searchable_text
                    for term in self.content_terms
                ):
                    continue
                external_id = str(
                    posting.get("reqId")
                    or posting.get("jobId")
                    or ""
                )
                title = str(posting.get("title") or "").strip()
                url = str(posting.get("applyUrl") or "")
                if not url and self.job_url_template and external_id:
                    url = self.job_url_template.format(
                        job_id=external_id,
                    )
                if not external_id or not title or not url:
                    continue
                if external_id in seen_external_ids:
                    continue

                seen_external_ids.add(external_id)
                jobs.append(
                    Job(
                        external_id=external_id,
                        company=self.company_name,
                        title=title,
                        url=url,
                        location=(
                            posting.get("location")
                            or posting.get("cityStateCountry")
                        ),
                        description=(
                            posting.get("description")
                            or posting.get("descriptionTeaser")
                        ),
                    )
                )

            offset += len(postings)
            total = int(search.get("totalHits") or 0)
            if not postings or offset >= total:
                break

        return jobs
