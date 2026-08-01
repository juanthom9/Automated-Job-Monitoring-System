from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT_SECONDS


def discover_company(
    name: str,
    careers_url: str,
    platform_hint: str | None = None,
) -> dict[str, Any]:
    # Create the basic company configuration
    company: dict[str, Any] = {
        "name": name.strip(),
        "careers_url": careers_url.strip(),
        "platform_hint": platform_hint,
        "enabled": True,
    }

    # First try the supplied URL directly
    direct_result = detect_from_url(
        company=company,
        url=careers_url,
    )

    if direct_result:
        return direct_result

    # Then inspect the careers page for ATS links
    discovered_urls = find_job_board_urls(careers_url)

    for discovered_url in discovered_urls:
        result = detect_from_url(
            company=company,
            url=discovered_url,
        )

        if result:
            # Keep the original official careers page
            result["careers_url"] = careers_url
            result["discovered_url"] = discovered_url
            return result

    # The platform is known, but its board URL was not found
    if platform_hint:
        company["connector"] = "unresolved"
        company["enabled"] = False
        company["discovery_status"] = (
            f"Platform hint found: {platform_hint}, "
            "but the underlying board URL was not detected"
        )

        return company

    # No supported platform could be detected
    company["connector"] = "unsupported"
    company["enabled"] = False
    company["discovery_status"] = (
        "No supported ATS platform was detected"
    )

    return company


def find_job_board_urls(careers_url: str) -> list[str]:
    # Download the official careers page
    try:
        response = httpx.get(
            careers_url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "User-Agent": "InternshipJobMonitor/1.0",
                "Accept": "text/html,application/xhtml+xml",
            },
        )

        response.raise_for_status()

    except httpx.HTTPError as error:
        print(
            f"Could not inspect {careers_url}: {error}"
        )
        return []

    discovered_urls: list[str] = [
        str(response.url),
    ]

    # Parse links and embedded resources
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    for tag in soup.find_all(
        ["a", "iframe", "script"],
    ):
        raw_url = (
            tag.get("href")
            or tag.get("src")
        )

        if not raw_url:
            continue

        full_url = urljoin(
            str(response.url),
            raw_url,
        )

        discovered_urls.append(full_url)

    # Search the page source for known ATS domains
    ats_domains = [
        "jobs.ashbyhq.com",
        "jobs.lever.co",
        "jobs.eu.lever.co",
        "boards.greenhouse.io",
        "job-boards.greenhouse.io",
        "myworkdayjobs.com",
        "careers.smartrecruiters.com",
        "jobs.smartrecruiters.com",
    ]

    page_source = response.text

    for domain in ats_domains:
        start = 0

        while True:
            index = page_source.find(domain, start)

            if index == -1:
                break

            # Capture text around the ATS domain
            beginning = page_source.rfind(
                "http",
                0,
                index,
            )

            ending_candidates = [
                page_source.find('"', index),
                page_source.find("'", index),
                page_source.find("<", index),
                page_source.find(" ", index),
            ]

            valid_endings = [
                ending
                for ending in ending_candidates
                if ending != -1
            ]

            if beginning != -1 and valid_endings:
                ending = min(valid_endings)

                discovered_urls.append(
                    page_source[beginning:ending]
                    .replace("\\/", "/")
                    .replace("\\u002F", "/")
                )

            start = index + len(domain)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(discovered_urls))


def detect_from_url(
    company: dict[str, Any],
    url: str,
) -> dict[str, Any] | None:
    # Parse the supplied or discovered URL
    parsed_url = urlparse(url)

    hostname = (
        parsed_url.hostname or ""
    ).lower()

    path_parts = [
        part
        for part in parsed_url.path.split("/")
        if part
    ]

    # Ashby
    if "ashbyhq.com" in hostname:
        if not path_parts:
            return None

        result = company.copy()
        result["connector"] = "ashby"
        result["board_name"] = path_parts[0]
        result["enabled"] = True
        result["discovery_status"] = "resolved"

        return result

    # Lever
    if "lever.co" in hostname:
        if not path_parts:
            return None

        result = company.copy()
        result["connector"] = "lever"
        result["site_name"] = path_parts[0]
        result["region"] = (
            "eu"
            if hostname.startswith("jobs.eu.")
            else "global"
        )
        result["enabled"] = True
        result["discovery_status"] = "resolved"

        return result

    # Greenhouse
    if "greenhouse.io" in hostname:
        ignored_parts = {
            "jobs",
            "job",
            "embed",
        }

        board_parts = [
            part
            for part in path_parts
            if part.lower() not in ignored_parts
        ]

        if not board_parts:
            return None

        result = company.copy()
        result["connector"] = "greenhouse"
        result["board_token"] = board_parts[0]
        result["enabled"] = True
        result["discovery_status"] = "resolved"

        return result

    # Workday
    if "myworkdayjobs.com" in hostname:
        ignored_parts = {
            "en-us",
            "en-ca",
            "fr-ca",
            "jobs",
            "job",
        }

        filtered_parts = [
            part
            for part in path_parts
            if part.lower() not in ignored_parts
        ]

        if not filtered_parts:
            return None

        tenant = hostname.split(".")[0]
        site_name = filtered_parts[0]

        result = company.copy()
        result["connector"] = "workday"
        result["api_url"] = (
            f"https://{hostname}/wday/cxs/"
            f"{tenant}/{site_name}/jobs"
        )
        result["public_base_url"] = (
            f"https://{hostname}/en-US/{site_name}"
        )
        result["enabled"] = True
        result["discovery_status"] = "resolved"

        return result

    # SmartRecruiters
    if "smartrecruiters.com" in hostname:
        ignored_parts = {
            "job",
            "jobs",
            "search",
        }
        identifier_parts = [
            part
            for part in path_parts
            if part.lower() not in ignored_parts
        ]

        if not identifier_parts:
            return None

        result = company.copy()
        result["connector"] = "smartrecruiters"
        result["company_identifier"] = identifier_parts[0]
        result["enabled"] = True
        result["discovery_status"] = "resolved"

        return result

    return None
