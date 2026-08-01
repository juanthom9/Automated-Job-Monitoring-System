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
        location="Various Locations within United States",
    )
    assert is_relevant_job(job)


def test_student_researcher_uses_description_for_technical_match():
    job = Job(
        external_id="researcher",
        company="Example",
        title="Student Researcher, BS/MS",
        url="https://example.com/researcher",
        location="Waterloo, ON, Canada",
        description="Currently pursuing a degree in Computer Science.",
    )
    assert is_relevant_job(job)


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


def test_college_grad_engineering_role_is_relevant():
    job = Job(
        external_id="college-grad",
        company="Example",
        title="Software Engineering AMTS (College Grad)",
        url="https://example.com/college-grad",
        location="California - San Francisco, US",
    )
    assert is_relevant_job(job)
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
