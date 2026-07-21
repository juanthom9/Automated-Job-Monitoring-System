from company_loader import load_companies
from connector_factory import create_connector


def main() -> None:
    # Load enabled companies
    companies = load_companies()

    for company in companies:
        connector = create_connector(company)

        # Download jobs using the correct connector
        jobs = connector.fetch_jobs()

        print(
            f"{company['name']}: "
            f"{len(jobs)} jobs found"
        )


if __name__ == "__main__":
    main()