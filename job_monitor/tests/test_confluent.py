from connectors.confluent import ConfluentConnector


def test_parse_page_maps_single_and_multiple_locations() -> None:
    html = """
    <div class="border-t py-4">
      <a href="/jobs/job/one"><p>Software Engineer Intern</p></a>
      <p>Remote, United States</p>
    </div>
    <div class="border-t py-4">
      <a href="/jobs/job/two"><p>Data Engineer Intern</p></a>
      <p>Available in Multiple Locations</p>
      <span>Toronto, Canada</span><span>Remote, United States</span>
    </div>
    """

    jobs = ConfluentConnector("Confluent")._parse_page(html)

    assert len(jobs) == 2
    assert jobs[0].external_id == "one"
    assert jobs[0].location == "Remote, United States"
    assert jobs[1].location == "Toronto, Canada; Remote, United States"
    assert jobs[1].url == "https://careers.confluent.io/jobs/job/two"
