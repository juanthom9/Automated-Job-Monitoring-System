from company_loader import load_companies


def main() -> None:
    # Load enabled companies from YAML
    companies = load_companies()

    print(f"Enabled companies: {len(companies)}")

    for company in companies:
        print(
            f"- {company['name']} "
            f"({company['connector']})"
        )


if __name__ == "__main__":
    main()