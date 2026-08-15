from typing import Any

import httpx

from config import REQUEST_TIMEOUT_SECONDS
from models import Job


class IBMConnector:
    API_URL = "https://www-api.ibm.com/search/api/v2"
    PAGE_SIZE = 100

    def __init__(
        self,
        company_name: str,
        countries: list[str] | None = None,
        experience_level: str = "Internship",
        search_query: str = "",
    ) -> None:
        self.company_name = company_name
        self.countries = countries or ["Canada", "United States"]
        self.experience_level = experience_level
        self.search_query = search_query

    def fetch_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        seen_external_ids: set[str] = set()
        offset = 0

        while True:
            response = httpx.post(
                self.API_URL,
                json=self._payload(offset),
                timeout=REQUEST_TIMEOUT_SECONDS,
                follow_redirects=True,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "InternshipJobMonitor/1.0",
                },
            )
            response.raise_for_status()
            result: dict[str, Any] = response.json()
            postings = (result.get("hits") or {}).get("hits")
            if not isinstance(postings, list):
                raise ValueError("IBM careers API returned an unexpected response")

            for posting in postings:
                job = self._map_job(posting)
                if job is None or job.external_id in seen_external_ids:
                    continue
                seen_external_ids.add(job.external_id)
                jobs.append(job)

            offset += len(postings)
            if not postings or len(postings) < self.PAGE_SIZE:
                break

        return jobs

    def _payload(self, offset: int) -> dict[str, Any]:
        country_terms = [
            {"term": {"field_keyword_05": country}}
            for country in self.countries
        ]
        filters: list[dict[str, Any]] = [
            {"bool": {"should": country_terms, "minimum_should_match": 1}},
            {"term": {"field_keyword_18": self.experience_level}},
        ]
        query_must: list[dict[str, Any]] = []
        if self.search_query:
            query_must.append(
                {
                    "multi_match": {
                        "query": self.search_query,
                        "fields": ["title^3", "description"],
                    }
                }
            )

        return {
            "appId": "careers",
            "scopes": ["careers2"],
            "query": {"bool": {"must": query_must}},
            "post_filter": {"bool": {"must": filters}},
            "size": self.PAGE_SIZE,
            "from": offset,
            "sort": [{"_score": "desc"}, {"pageviews": "desc"}],
            "lang": "zz",
            "localeSelector": {},
            "sm": {"query": self.search_query, "lang": "zz"},
            "_source": [
                "_id",
                "title",
                "url",
                "description",
                "field_keyword_05",
                "field_keyword_08",
                "field_keyword_17",
                "field_keyword_18",
                "field_keyword_19",
            ],
        }

    def _map_job(self, posting: dict[str, Any]) -> Job | None:
        source = posting.get("_source") or {}
        external_id = str(source.get("_id") or posting.get("_id") or "")
        title = str(source.get("title") or "").strip()
        url = str(source.get("url") or "").strip()
        if not external_id or not title or not url.startswith(("http://", "https://")):
            return None

        return Job(
            external_id=external_id,
            company=self.company_name,
            title=title,
            url=url,
            location=source.get("field_keyword_19"),
            description=source.get("description"),
        )
