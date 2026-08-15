from connectors.successfactors import SuccessFactorsConnector


def test_parse_page_maps_successfactors_search_row():
    html = """
    <table>
      <tr class="data-row">
        <td class="colTitle">
          <span class="jobTitle">
            <a class="jobTitle-link" href="/job/Vancouver-Developer/12345/">
              Software Developer Intern
            </a>
          </span>
        </td>
        <td class="colLocation">
          <span class="jobLocation">Vancouver, British Columbia, CA</span>
        </td>
      </tr>
    </table>
    """

    jobs = SuccessFactorsConnector(
        "SAP",
        "https://jobs.example.com/",
    )._parse_page(html)

    assert len(jobs) == 1
    assert jobs[0].external_id == "12345"
    assert jobs[0].title == "Software Developer Intern"
    assert jobs[0].location == "Vancouver, British Columbia, CA"
    assert jobs[0].url == "https://jobs.example.com/job/Vancouver-Developer/12345/"
