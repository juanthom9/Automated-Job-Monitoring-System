from company_loader import load_all_companies, save_companies
from connector_factory import create_connector


def main() -> None:
    # Load every configured company
    companies = load_all_companies()

    validated = 0
    failed = 0
    skipped = 0

    for company in companies:
        if not company.get("enabled", True):
            skipped += 1
            continue

        company_name = company["name"]

        try:
            # Create the detected connector
            connector = create_connector(company)

            # Confirm that the connector returns a job list
            jobs = connector.fetch_jobs()

            company["validation_status"] = "valid"
            company["validation_error"] = None
            company["last_job_count"] = len(jobs)

            validated += 1

            print(
                f"{company_name}: valid | "
                f"{company['connector']} | "
                f"{len(jobs)} jobs"
            )

        except Exception as error:
            # Disable broken or incorrectly detected boards
            company["enabled"] = False
            company["validation_status"] = "failed"
            company["validation_error"] = str(error)

            failed += 1

            print(
                f"{company_name}: FAILED | "
                f"{company['connector']} | "
                f"{error}"
            )

    # Save validation results to companies.yaml
    save_companies(companies)

    print("\nValidation completed.")
    print(f"Validated: {validated}")
    print(f"Failed and disabled: {failed}")
    print(f"Already disabled: {skipped}")


if __name__ == "__main__":
    main()