from pathlib import Path
from typing import Any

from company_discovery import discover_company
from company_loader import add_or_update_company


def import_company_file(file_path: str) -> dict[str, int]:
    # Convert the supplied path to a Path object
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(
            f"Company file was not found: {path}"
        )

    imported_count = 0
    supported_count = 0
    unsupported_count = 0
    skipped_count = 0

    with path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            # Ignore blank lines and headings
            if (
                not line
                or line.startswith("OFFICIAL COMPANY")
                or line.startswith("Format:")
            ):
                continue

            parts = [
                part.strip()
                for part in line.split("|")
            ]

            # Every company requires at least a name and URL
            if len(parts) < 2:
                print(
                    f"Line {line_number} skipped: "
                    "invalid format"
                )
                skipped_count += 1
                continue

            name = parts[0]
            careers_url = parts[1]

            platform_hint = (
                parts[2]
                if len(parts) >= 3 and parts[2]
                else None
            )

            if not name or not careers_url:
                print(
                    f"Line {line_number} skipped: "
                    "missing name or URL"
                )
                skipped_count += 1
                continue

            try:
                # Detect the ATS from the official URL
                company = discover_company(
                    name=name,
                    careers_url=careers_url,
                    platform_hint=platform_hint,
                )

                if platform_hint:
                    company["platform_hint"] = platform_hint

                # Do not monitor unresolved boards yet
                if company["connector"] in {
                    "unsupported",
                    "unresolved",
                }:
                    company["enabled"] = False
                    unsupported_count += 1
                else:
                    company["enabled"] = True
                    supported_count += 1

                add_or_update_company(company)
                imported_count += 1

                print(
                    f"{name}: "
                    f"{company['connector']} | "
                    f"{'enabled' if company['enabled'] else 'disabled'}"
                )

            except Exception as error:
                print(
                    f"Line {line_number} failed "
                    f"for {name}: {error}"
                )
                skipped_count += 1

    return {
        "imported": imported_count,
        "supported": supported_count,
        "unsupported": unsupported_count,
        "skipped": skipped_count,
    }