from pathlib import Path
from typing import Any

import yaml


COMPANIES_FILE = Path(__file__).parent / "companies.yaml"


def load_all_companies() -> list[dict[str, Any]]:
    # Read all companies from the YAML file
    if not COMPANIES_FILE.exists():
        return []

    with COMPANIES_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = yaml.safe_load(file) or {}

    companies = data.get("companies", [])

    if not isinstance(companies, list):
        raise ValueError(
            "The companies field in companies.yaml must be a list"
        )

    return companies


def load_companies() -> list[dict[str, Any]]:
    # Return only companies that are enabled
    return [
        company
        for company in load_all_companies()
        if company.get("enabled", True)
    ]


def save_companies(
    companies: list[dict[str, Any]],
) -> None:
    # Save all companies back to the YAML file
    data = {
        "companies": companies,
    }

    with COMPANIES_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            data,
            file,
            sort_keys=False,
            allow_unicode=True,
        )


def add_or_update_company(
    company: dict[str, Any],
) -> None:
    # Add a new company or update an existing one
    companies = load_all_companies()

    for index, existing_company in enumerate(companies):
        if (
            existing_company["name"].lower()
            == company["name"].lower()
        ):
            companies[index] = company
            save_companies(companies)
            return

    companies.append(company)
    save_companies(companies)