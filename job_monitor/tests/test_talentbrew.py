from connectors.talentbrew import TalentBrewConnector


def test_parse_page_maps_talentbrew_result_and_pagination() -> None:
    html = """
    <section data-selector-name="searchresults" data-total-pages="3">
      <a data-job-id="123" href="/en/job/wichita/software-intern/1/123">
        <h3>Software Engineer Intern</h3>
        <span class="job-location">Wichita, Kansas, United States</span>
      </a>
    </section>
    """

    jobs, total_pages = TalentBrewConnector(
        "NetApp",
        "https://careers.example.com/en/search-jobs",
    )._parse_page(html)

    assert total_pages == 3
    assert len(jobs) == 1
    assert jobs[0].external_id == "123"
    assert jobs[0].location == "Wichita, Kansas, United States"
    assert jobs[0].url == (
        "https://careers.example.com/en/job/wichita/software-intern/1/123"
    )
