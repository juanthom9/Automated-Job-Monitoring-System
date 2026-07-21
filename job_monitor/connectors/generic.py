from __future__ import annotations

import hashlib
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from ..models import Company, Job
from .base import Connector


class GenericConnector(Connector):
    """Fallback for server-rendered career pages.

    Configure `careers_url` and optionally `job_link_selector`.
    This intentionally avoids guessing on heavily JavaScript-driven sites.
    """

    def fetch(self, company: Company) -> list[Job]:
        careers_url = str(company.settings["careers_url"])
        selector = str(company.settings.get("job_link_selector", "a[href]"))
        response = self.client.get(careers_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        host = urlparse(careers_url).netloc
        jobs: list[Job] = []
        seen_urls: set[str] = set()
        for anchor in soup.select(selector):
            title = anchor.get_text(" ", strip=True)
            href = anchor.get("href")
            if not title or not href:
                continue
            absolute = urljoin(careers_url, href)
            parsed = urlparse(absolute)
            if parsed.netloc != host and not company.settings.get("allow_external_links", True):
                continue
            lower = f"{title} {absolute}".lower()
            if not any(word in lower for word in ("job", "career", "position", "opening", "intern", "co-op")):
                continue
            if absolute in seen_urls:
                continue
            seen_urls.add(absolute)
            external_id = hashlib.sha256(absolute.encode("utf-8")).hexdigest()[:24]
            jobs.append(
                Job(
                    company=company.name,
                    external_id=external_id,
                    title=title,
                    location="",
                    url=absolute,
                )
            )
        return jobs
