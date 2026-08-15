from connectors.mathworks import MathWorksConnector


def test_parse_page_maps_and_normalizes_mathworks_result() -> None:
    html = """
    <table><tr>
      <td class="search_result_desc">
        <div class="search_title">
          <a href="/company/jobs/opportunities/37078-security-intern">
            Security Engineering Intern
          </a>
        </div>
        <div class="additional_field">
          <span>US-MA-Natick</span> | Information Technology | Internships
        </div>
        <div class="search_highlight">Build security automation.</div>
      </td>
    </tr></table>
    """

    jobs = MathWorksConnector("MathWorks")._parse_page(html)

    assert len(jobs) == 1
    assert jobs[0].external_id == "37078"
    assert jobs[0].location == "Natick, MA, USA"
    assert jobs[0].description == "Build security automation."
    assert jobs[0].url.endswith("/37078-security-intern")
