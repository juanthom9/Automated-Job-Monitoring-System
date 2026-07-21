from database import Database


def main() -> None:
    database = Database()

    # Add a temporary company
    company = database.add_company(
        name="Wealthsimple",
        careers_url="https://jobs.lever.co/wealthsimple",
        connector="lever",
        platform_hint="Lever",
    )

    print("Company saved:")
    print(company)

    # Display all enabled companies
    companies = database.get_enabled_companies()

    print("\nEnabled companies:")

    for saved_company in companies:
        print(
            f"- {saved_company['name']} "
            f"({saved_company['connector']})"
        )


if __name__ == "__main__":
    main()