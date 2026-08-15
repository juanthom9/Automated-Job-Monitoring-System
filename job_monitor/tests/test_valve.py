from connectors.valve import ValveConnector


def test_parse_page_deduplicates_roles_and_extracts_ids():
    html = """
    <a href="https://www.valvesoftware.com/en/jobs?job_id=14">Steam Software Engineer</a>
    <a href="https://www.valvesoftware.com/en/jobs?job_id=14">Steam Software Engineer</a>
    <a href="https://www.valvesoftware.com/en/jobs?job_id=51">Game Developer</a>
    """

    jobs = ValveConnector("Valve")._parse_page(html)

    assert [job.external_id for job in jobs] == ["14", "51"]
    assert jobs[0].location == "Bellevue, WA, USA"
