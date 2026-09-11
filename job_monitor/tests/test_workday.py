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


def test_applied_facets_are_sent_with_search_request(monkeypatch):
    captured_json = None

    def fake_post(*args, **kwargs):
        nonlocal captured_json
        captured_json = kwargs["json"]
        return FakeResponse({"total": 0, "jobPostings": []})

    monkeypatch.setattr("connectors.workday.httpx.post", fake_post)

    facets = {
        "locationCountry": ["canada-id"],
        "jobFamily": ["campus-id", "interns-id"],
    }
    WorkdayConnector(
        "Example",
        "https://example.com/wday/cxs/example/site/jobs",
        "https://example.com/en-US/site",
        applied_facets=facets,
    ).fetch_jobs()

    assert captured_json is not None
    assert captured_json["appliedFacets"] == facets


def test_pagination_keeps_total_from_first_page(monkeypatch):
    requested_offsets = []

    def fake_post(*args, **kwargs):
        offset = kwargs["json"]["offset"]
        requested_offsets.append(offset)
        page_size = 20 if offset < 40 else 5
        postings = [
            {
                "title": f"Software Engineer Intern {offset + index}",
                "externalPath": f"/job/intern-{offset + index}",
                "locationsText": "Toronto, Ontario, Canada",
                "bulletFields": [f"R{offset + index}"],
            }
            for index in range(page_size)
        ]
        return FakeResponse({
            "total": 45 if offset == 0 else 0,
            "jobPostings": postings,
        })

    monkeypatch.setattr("connectors.workday.httpx.post", fake_post)

    jobs = WorkdayConnector(
        "Example",
        "https://example.com/wday/cxs/example/site/jobs",
        "https://example.com/en-US/site",
    ).fetch_jobs()

    assert requested_offsets == [0, 20, 40]
    assert len(jobs) == 45
