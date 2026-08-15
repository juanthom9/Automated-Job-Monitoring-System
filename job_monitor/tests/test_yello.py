from connectors.yello import YelloConnector


def test_parse_results_extracts_requisition_and_job():
    html = """
    <li class="search-results__item">
      <div class="search-results__jobinfo">
        <a class="search-results__req_title" href="/jobs/abc?job_board_id=board">
          Technology Risk - Canada - Internship Co-op
        </a>
        <div><span>1736015</span></div>
      </div>
    </li>
    """

    connector = YelloConnector("EY", "board", [1, 2])
    jobs = connector._parse_results(html)

    assert len(jobs) == 1
    assert jobs[0].external_id == "1736015"
    assert jobs[0].location == "Canada"
