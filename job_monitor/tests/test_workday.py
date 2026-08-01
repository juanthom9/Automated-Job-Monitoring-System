from connectors.workday import WorkdayConnector


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


def test_multi_location_posting_uses_public_detail(monkeypatch):
    search_response = FakeResponse({
        "total": 1,
        "jobPostings": [{
            "title": "Machine Learning Intern",
            "externalPath": "/job/San-Jose/intern_R1",
            "locationsText": "3 Locations",
            "bulletFields": ["R1"],
        }],
    })
    detail_response = FakeResponse({
        "jobPostingInfo": {
            "location": "San Jose",
            "additionalLocations": ["Seattle", "San Francisco"],
            "jobDescription": "<p>Build machine learning systems.</p>",
        }
    })
    monkeypatch.setattr(
        "connectors.workday.httpx.post",
        lambda *args, **kwargs: search_response,
    )
    monkeypatch.setattr(
        "connectors.workday.httpx.get",
        lambda *args, **kwargs: detail_response,
    )

    jobs = WorkdayConnector(
        "Example",
        "https://example.com/wday/cxs/example/site/jobs",
        "https://example.com/en-US/site",
        ["internship"],
    ).fetch_jobs()

    assert jobs[0].location == "San Jose; Seattle; San Francisco"
    assert jobs[0].description == "Build machine learning systems."
