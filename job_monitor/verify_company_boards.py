from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from company_discovery import detect_from_url, find_job_board_urls
from company_loader import load_all_companies
from connector_factory import create_connector


@dataclass
class Verification:
    name: str
    configured_connector: str
    discovered_connector: str | None
    jobs_found: int | None
    status: str
    detail: str


def discover_official_connector(company: dict[str, Any]) -> tuple[str | None, str]:
    # Only a direct ATS careers URL can establish a platform mismatch by
    # itself. Company careers pages often link to subsidiaries that use a
    # different ATS (for example, Cisco linking to Splunk roles).
    direct = detect_from_url(company, str(company["careers_url"]))
    if direct:
        return str(direct["connector"]), str(company["careers_url"])

    candidates = find_job_board_urls(str(company["careers_url"]))
    discoveries: list[tuple[str, str]] = []

    for url in candidates:
        result = detect_from_url(company, url)
        if result:
            discoveries.append((str(result["connector"]), url))

    configured = str(company.get("connector", "")).lower()
    for connector, url in discoveries:
        if connector == configured:
            return connector, url

    return None, "No supported ATS link was exposed by the careers page"


def verify_company(company: dict[str, Any]) -> Verification:
    name = str(company["name"])
    configured = str(company.get("connector", "unknown")).lower()

    if not company.get("enabled", True):
        return Verification(
            name, configured, None, None, "disabled",
            "Company is intentionally disabled or unresolved",
        )

    discovered, evidence = discover_official_connector(company)

    try:
        jobs = create_connector(company).fetch_jobs()
        count = len(jobs)
    except Exception as error:
        return Verification(
            name, configured, discovered, None, "connector_failed",
            f"{type(error).__name__}: {error}",
        )

    if discovered and discovered != configured:
        return Verification(
            name, configured, discovered, count, "platform_mismatch",
            evidence,
        )

    if count == 0:
        status = "empty_official" if discovered == configured else "empty_unconfirmed"
        return Verification(name, configured, discovered, count, status, evidence)

    if discovered == configured:
        return Verification(name, configured, discovered, count, "confirmed", evidence)

    return Verification(
        name, configured, discovered, count, "live_unconfirmed", evidence,
    )


def escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_report(results: list[Verification]) -> Path:
    output = Path("board-verification-report.md")
    status_counts: dict[str, int] = {}
    for result in results:
        status_counts[result.status] = status_counts.get(result.status, 0) + 1

    lines = [
        "# Job board verification report",
        "",
        "A live connector proves that an endpoint works. `confirmed` additionally means the",
        "official careers path exposed the same supported ATS. Other live boards require",
        "manual ownership verification before they should be considered fully confirmed.",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")

    lines.extend([
        "",
        "## Companies",
        "",
        "| Company | Configured | Discovered | Jobs | Status | Evidence / detail |",
        "|---|---|---|---:|---|---|",
    ])
    for result in sorted(results, key=lambda item: (item.status, item.name.lower())):
        lines.append(
            f"| {escape(result.name)} | {escape(result.configured_connector)} | "
            f"{escape(result.discovered_connector or '')} | "
            f"{'' if result.jobs_found is None else result.jobs_found} | "
            f"{escape(result.status)} | {escape(result.detail)} |"
        )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main() -> None:
    companies = load_all_companies()
    results: list[Verification] = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(verify_company, company): company["name"]
            for company in companies
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"{result.name}: {result.status} | "
                f"{result.jobs_found if result.jobs_found is not None else '-'} jobs"
            )

    report = write_report(results)
    print(f"Verified {len(results)} companies. Report: {report.resolve()}")


if __name__ == "__main__":
    main()
