from filters import is_canadian_location
from filters import is_relevant_job
from filters import is_canada_or_us_location


def test_explicit_foreign_country_overrides_ambiguous_city():
    assert not is_canada_or_us_location(
        "Melbourne, Victoria, AUS"
    )


def test_iso_canada_and_us_locations_are_accepted():
    assert is_canada_or_us_location("Toronto, Ontario, CAN")
    assert is_canada_or_us_location("Seattle, Washington, USA")


def test_iso_alpha_two_foreign_country_codes_are_rejected():
    assert not is_canada_or_us_location("IN")
    assert not is_canada_or_us_location("Al Asimah Governate,KW")
    assert not is_canada_or_us_location("Rusayl, Muscat Governorate, OM")
    assert is_canada_or_us_location("Cambridge, MA, US")
    assert is_canada_or_us_location("Québec City, QC, CA")


def test_explicit_foreign_country_beats_state_name():
    assert not is_canada_or_us_location(
        "Tijuana, Baja California, Mexico"
    )
    assert not is_canada_or_us_location(
        "Hod Hasharon, Haifa District, Israel"
    )


def test_plural_internships_title_is_relevant():
    job = Job(
        external_id="plural",
        company="Example",
        title="Machine Learning Engineering Internships",
        url="https://example.com/plural",
        location="Various Locations within Canada",
    )
    assert is_relevant_job(job)


def test_americas_internship_is_not_in_canadian_target_region():
    job = Job(
        external_id="shopify-1",
        company="Shopify",
        title="Applied Machine Learning Engineering Internships",
        url="https://example.com/job",
        location="Americas",
    )

    assert not is_relevant_job(job)


def test_student_researcher_is_not_an_internship_or_coop():
    job = Job(
        external_id="researcher",
        company="Example",
        title="Student Researcher, BS/MS",
        url="https://example.com/researcher",
        location="Waterloo, ON, Canada",
        description="Currently pursuing a degree in Computer Science.",
    )
    assert not is_relevant_job(job)


def test_product_management_intern_is_not_technical_role():
    job = Job(
        external_id="product",
        company="Example",
        title="Product Management Intern",
        url="https://example.com/product",
        location="San Francisco, CA, US",
        description="Collaborate closely with software engineering teams.",
    )
    assert not is_relevant_job(job)


def test_non_engineering_titles_are_not_technical_from_description():
    for title in (
        "Product Designer, Internship",
        "Deployment Strategist, Internship",
    ):
        job = Job(
            external_id=title,
            company="Example",
            title=title,
            url="https://example.com/role",
            location="New York, NY, US",
            description="Collaborate with software engineers on infrastructure.",
        )
        assert not is_relevant_job(job)


def test_college_grad_engineering_role_is_not_relevant():
    job = Job(
        external_id="college-grad",
        company="Example",
        title="Software Engineering AMTS (College Grad)",
        url="https://example.com/college-grad",
        location="Toronto, ON, Canada",
    )
    assert not is_relevant_job(job)
from models import Job


def main() -> None:
    jobs = [
        Job(
            external_id="1",
            company="Example",
            title="Software Engineer Intern",
            url="https://example.com/1",
            location="Toronto, ON, Canada",
        ),
        Job(
            external_id="2",
            company="Example",
            title="Machine Learning Intern",
            url="https://example.com/2",
            location="San Francisco, CA",
        ),
        Job(
            external_id="3",
            company="Example",
            title="University Recruiter",
            url="https://example.com/3",
            location="New York, NY",
            description="Recruit software engineering interns.",
        ),
        Job(
            external_id="4",
            company="Example",
            title="Marketing Intern",
            url="https://example.com/4",
            location="Toronto, Canada",
        ),
        Job(
            external_id="5",
            company="Example",
            title="Software Engineer Intern",
            url="https://example.com/5",
            location="London, United Kingdom",
        ),
    ]

    for job in jobs:
        print(
            f"{job.title} | {job.location}: "
            f"{is_relevant_job(job)}"
        )


if __name__ == "__main__":
    main()


def test_rejects_new_grad_banker_with_technical_description() -> None:
    job = Job(
        external_id="banker-1",
        company="Example Bank",
        title="Retail Relationship Banker (New Grad)",
        url="https://example.com/jobs/banker-1",
        location="Milwaukee, WI, USA",
        description="Supports customers using banking technology and systems.",
    )

    assert not is_relevant_job(job)


def test_accepts_business_intelligence_coop() -> None:
    job = Job(
        external_id="bi-coop-1",
        company="Example",
        title="Business Intelligence Internship/Co-Op",
        url="https://example.com/jobs/bi-coop-1",
        location="Toronto, ON, Canada",
    )

    assert is_relevant_job(job)


def test_accepts_research_scientist_internship() -> None:
    job = Job(
        external_id="research-intern-1",
        company="Example",
        title="PhD Research Scientist Intern",
        url="https://example.com/jobs/research-intern-1",
        location="Toronto, ON, Canada",
    )

    assert is_relevant_job(job)


def test_accepts_network_engineering_internship() -> None:
    job = Job(
        external_id="network-intern-1",
        company="Example",
        title="Networks CNS Intern",
        url="https://example.com/jobs/network-intern-1",
        location="Ottawa, ON, Canada",
    )

    assert is_relevant_job(job)


def test_rejects_internship_with_full_us_state_name() -> None:
    job = Job(
        external_id="kansas-intern-1",
        company="Example",
        title="Software Engineer Intern",
        url="https://example.com/jobs/kansas-intern-1",
        location="Olathe, Kansas",
    )

    assert not is_relevant_job(job)


def test_rejects_dutch_nh_as_new_hampshire() -> None:
    job = Job(
        external_id="amsterdam-intern-1",
        company="Example",
        title="Data Analyst Intern",
        url="https://example.com/jobs/amsterdam-intern-1",
        location="Amsterdam, NH",
        description="Analyze software and cloud platform data.",
    )

    assert not is_relevant_job(job)


def test_accepts_security_operations_engineering_internship() -> None:
    job = Job(
        external_id="security-ops-intern-1",
        company="Example",
        title="Security Operations & Engineering Fall Intern",
        url="https://example.com/jobs/security-ops-intern-1",
        location="Waterloo, ON, Canada",
    )

    assert is_relevant_job(job)


def test_rejects_business_operations_internship() -> None:
    job = Job(
        external_id="business-ops-intern-1",
        company="Example",
        title="Business Operations Intern",
        url="https://example.com/jobs/business-ops-intern-1",
        location="Austin, TX, USA",
        description="Work with software and cloud teams.",
    )

    assert not is_relevant_job(job)


def test_rejects_accounting_roles_with_generic_technical_descriptions() -> None:
    excluded_titles = [
        "CPA Opportunities in Audit - Co-op",
        "Canadian Tax - Internship",
        "Technology Risk Services Intern/Co-op",
        "Actuarial Intern/Co-op",
    ]
    for title in excluded_titles:
        job = Job(
            external_id=title,
            company="KPMG",
            title=title,
            url="https://example.com/job",
            location="Toronto, Canada",
            description="Work with software, cloud, data, and cybersecurity teams.",
        )
        assert not is_relevant_job(job)


def test_rejects_technical_student_contract_worker() -> None:
    job = Job(
        external_id="student-worker-1",
        company="Example",
        title="Contract Student Worker - Machine Learning Engineer",
        url="https://example.com/jobs/student-worker-1",
        location="Toronto, ON, Canada",
    )

    assert not is_relevant_job(job)


def test_canada_only_location_filter_rejects_us_and_accepts_canada() -> None:
    assert is_canadian_location("Toronto, ON, Canada")
    assert is_canadian_location("Montreal, QC, CA")
    assert not is_canadian_location("San Francisco, CA, US")
    assert not is_canadian_location("Foster City, CA")


def test_rejects_slovak_sk_postcode_as_saskatchewan() -> None:
    job = Job(
        external_id="slovakia-1",
        company="Example",
        title="Software R&D Intern",
        url="https://example.com/jobs/slovakia-1",
        location="Zilina, SK, 010 01",
    )

    assert not is_relevant_job(job)
