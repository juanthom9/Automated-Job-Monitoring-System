from connectors.intuit import IntuitConnector


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


def test_fetch_jobs_maps_cards_and_deduplicates_searches(monkeypatch):
    page = """
    <a class="sr-item" data-job-id="22401"
       href="/job/toronto/software-developer-co-op/27595/97137794368">
      <h2>Software Developer Co-op</h2>
      <span class="job-location">Toronto, Canada</span>
    </a>
    """
    monkeypatch.setattr(
        "connectors.intuit.httpx.get",
        lambda *args, **kwargs: FakeResponse(page),
    )

    jobs = IntuitConnector("Intuit").fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "97137794368"
    assert jobs[0].company == "Intuit"
    assert jobs[0].title == "Software Developer Co-op"
    assert jobs[0].location == "Toronto, Canada"
    assert jobs[0].url == (
        "https://jobs.intuit.com/job/toronto/"
        "software-developer-co-op/27595/97137794368"
    )


def test_fetch_jobs_skips_incomplete_cards(monkeypatch):
    page = '<a class="sr-item" data-job-id=""><h2></h2></a>'
    monkeypatch.setattr(
        "connectors.intuit.httpx.get",
        lambda *args, **kwargs: FakeResponse(page),
    )

    assert IntuitConnector("Intuit").fetch_jobs() == []
