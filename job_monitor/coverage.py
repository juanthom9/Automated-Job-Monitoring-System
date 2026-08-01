from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any


WORKING_CONNECTORS = {
    "ashby",
    "amazon",
    "apple",
    "eightfold",
    "google",
    "greenhouse",
    "lever",
    "microsoft",
    "netflix",
    "phenom",
    "smartrecruiters",
    "workday",
}


def classify_company(company: dict[str, Any]) -> str:
    connector = str(company.get("connector", "")).lower()

    if (
        company.get("enabled", True)
        and connector in WORKING_CONNECTORS
        and company.get("validation_status") != "failed"
    ):
        if company.get("validation_status") == "valid":
            return "validated"
        return "configured_unvalidated"

    if company.get("validation_status") == "failed":
        return "configured_failing"

    if connector == "unresolved":
        return "needs_investigation"

    if connector == "unsupported":
        return "needs_connector"

    return "disabled_or_unknown"


def build_coverage_report(
    companies: list[dict[str, Any]],
) -> str:
    rows = [
        {
            "name": company["name"],
            "platform": company.get("platform_hint") or "Unknown",
            "connector": company.get("connector") or "Unknown",
            "status": classify_company(company),
            "jobs": company.get("last_job_count", ""),
            "url": company.get("careers_url", ""),
        }
        for company in companies
    ]
    counts = Counter(row["status"] for row in rows)

    lines = [
        "# Company coverage report",
        "",
        f"Total companies: **{len(rows)}**",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]

    for status in (
        "validated",
        "configured_unvalidated",
        "configured_failing",
        "needs_investigation",
        "needs_connector",
        "disabled_or_unknown",
    ):
        lines.append(f"| {status} | {counts[status]} |")

    lines.extend(
        [
            "",
            "## Companies",
            "",
            "| Company | Claimed platform | Connector | Status | Last jobs | Careers page |",
            "|---|---|---|---|---:|---|",
        ]
    )

    for row in sorted(rows, key=lambda item: (item["status"], item["name"])):
        name = str(row["name"]).replace("|", "\\|")
        platform = str(row["platform"]).replace("|", "\\|")
        connector = str(row["connector"]).replace("|", "\\|")
        url = str(row["url"])
        link = f"[official page]({url})" if url else ""
        lines.append(
            f"| {name} | {platform} | {connector} | "
            f"{row['status']} | {row['jobs']} | {link} |"
        )

    return "\n".join(lines) + "\n"


def write_coverage_report(
    companies: list[dict[str, Any]],
    output_path: str | Path,
) -> Path:
    path = Path(output_path).resolve()
    path.write_text(
        build_coverage_report(companies),
        encoding="utf-8",
    )
    return path
