from connectors.microsoft import MicrosoftConnector


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


def test_fetch_jobs_maps_and_paginates_positions(monkeypatch):
    posting = {
        "id": 1970393556867858,
        "atsJobId": "200037837",
        "displayJobId": "200037837",
        "name": "Research Intern - Self-Improving AI",
        "standardizedLocations": ["Cambridge, MA, US", "New York, NY, US"],
        "postedTs": 1779139945,
        "positionUrl": "/careers/job/1970393556867858",
    }
    responses = [
        FakeResponse({"data": {"count": 2, "positions": [posting]}}),
        FakeResponse({"data": {"count": 2, "positions": [
            {**posting, "id": 2, "atsJobId": "200037838"}
        ]}}),
    ]
    monkeypatch.setattr(
        "connectors.microsoft.httpx.get",
        lambda *args, **kwargs: responses.pop(0),
    )

    jobs = MicrosoftConnector("Microsoft").fetch_jobs()

    assert len(jobs) == 2
    assert jobs[0].external_id == "200037837"
    assert jobs[0].location == "Cambridge, MA, US; New York, NY, US"
    assert jobs[0].url.endswith("/careers/job/1970393556867858")
    assert jobs[0].posted_at is not None
