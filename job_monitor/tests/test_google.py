from connectors.google import GoogleConnector


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


def test_fetch_jobs_maps_google_card_and_stops(monkeypatch):
    first_page = """
    <div class="sMn82b">
      <h3>Student Researcher, BS/MS</h3>
      <span class="r0wTof">Waterloo, ON, Canada</span>
      <ul><li>Currently pursuing a degree in Computer Science.</li></ul>
      <a href="jobs/results/123456-student-researcher">Learn more</a>
    </div>
    """
    responses = [FakeResponse(first_page), FakeResponse("")]
    monkeypatch.setattr(
        "connectors.google.httpx.get",
        lambda *args, **kwargs: responses.pop(0),
    )

    jobs = GoogleConnector("Google").fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "123456"
    assert jobs[0].location == "Waterloo, ON, Canada"
    assert jobs[0].url.endswith(
        "/applications/jobs/results/123456-student-researcher"
    )
