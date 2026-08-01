from connectors.apple import AppleConnector


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


def test_fetch_jobs_maps_apple_card_and_stops(monkeypatch):
    first_page = """
    <div class="job-title job-list-item">
      <h3><a href="/en-ca/details/200123-3350/software-intern">
        Software Engineering Intern
      </a></h3>
      <div class="job-title-location">
        <span class="a11y">Location</span><span>Vancouver</span>
      </div>
    </div>
    """
    responses = [FakeResponse(first_page), FakeResponse("")]
    monkeypatch.setattr(
        "connectors.apple.httpx.get",
        lambda *args, **kwargs: responses.pop(0),
    )

    jobs = AppleConnector("Apple").fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "200123-3350"
    assert jobs[0].title == "Software Engineering Intern"
    assert jobs[0].location == "Vancouver"
    assert jobs[0].url.startswith("https://jobs.apple.com/")
