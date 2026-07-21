import argparse

from company_discovery import discover_company
from company_importer import import_company_file
from company_loader import (
    add_or_update_company,
    load_all_companies,
)


def add_company(
    name: str,
    url: str,
) -> None:
    # Detect the company job-board platform
    company = discover_company(
        name=name,
        careers_url=url,
    )

    # Save or update the company in companies.yaml
    add_or_update_company(company)

    print(f"Saved company: {company['name']}")
    print(f"Connector: {company['connector']}")

    if company["connector"] == "unsupported":
        print(
            "This company uses a custom or unresolved job board. "
            "A dedicated connector may be required."
        )


def list_companies() -> None:
    # Load every configured company
    companies = load_all_companies()

    if not companies:
        print("No companies have been added.")
        return

    print(f"Configured companies: {len(companies)}")

    for company in companies:
        status = (
            "enabled"
            if company.get("enabled", True)
            else "disabled"
        )

        print(
            f"- {company['name']} | "
            f"{company['connector']} | "
            f"{status}"
        )


def import_companies(file_path: str) -> None:
    # Import companies from the supplied text file
    results = import_company_file(file_path)

    print("\nImport completed.")
    print(f"Companies imported: {results['imported']}")
    print(f"Supported and enabled: {results['supported']}")
    print(
        f"Unsupported and disabled: "
        f"{results['unsupported']}"
    )
    print(f"Lines skipped: {results['skipped']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage internship job-monitor companies"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Add or update one company
    add_parser = subparsers.add_parser(
        "add-company",
        help="Add or update a company",
    )

    add_parser.add_argument(
        "--name",
        required=True,
        help="Company name",
    )

    add_parser.add_argument(
        "--url",
        required=True,
        help="Official company job-board URL",
    )

    # Display all configured companies
    subparsers.add_parser(
        "list-companies",
        help="List configured companies",
    )

    # Import companies from a text file
    import_parser = subparsers.add_parser(
        "import-file",
        help="Import companies from a text file",
    )

    import_parser.add_argument(
        "--file",
        required=True,
        help="Path to the company job-board text file",
    )

    args = parser.parse_args()

    if args.command == "add-company":
        add_company(
            name=args.name,
            url=args.url,
        )

    elif args.command == "list-companies":
        list_companies()

    elif args.command == "import-file":
        import_companies(
            file_path=args.file,
        )


if __name__ == "__main__":
    main()