from connectors.smartrecruiters import SmartRecruitersConnector


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


def test_fetch_jobs_maps_postings_and_location(monkeypatch):
    payload = {
        "totalFound": 1,
        "content": [
            {
                "id": "744000123",
                "name": "Software Engineering Intern",
                "location": {
                    "city": "Montreal",
                    "region": "QC",
                    "country": "ca",
                    "remote": True,
                },
            }
        ],
    }

    monkeypatch.setattr(
        "connectors.smartrecruiters.httpx.get",
        lambda *args, **kwargs: FakeResponse(payload),
    )

    connector = SmartRecruitersConnector(
        company_name="Example",
        company_identifier="ExampleCompany",
    )
    jobs = connector.fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "744000123"
    assert jobs[0].title == "Software Engineering Intern"
    assert jobs[0].location == "Montreal, QC, ca, Remote"
    assert jobs[0].url == (
        "https://jobs.smartrecruiters.com/"
        "ExampleCompany/744000123"
    )


def test_fetch_jobs_paginates(monkeypatch):
    payloads = [
        {
            "totalFound": 2,
            "content": [{"id": "1", "name": "First"}],
        },
        {
            "totalFound": 2,
            "content": [{"id": "2", "name": "Second"}],
        },
    ]

    def fake_get(*args, **kwargs):
        return FakeResponse(payloads.pop(0))

    monkeypatch.setattr(
        "connectors.smartrecruiters.httpx.get",
        fake_get,
    )

    connector = SmartRecruitersConnector("Example", "example")
    jobs = connector.fetch_jobs()

    assert [job.external_id for job in jobs] == ["1", "2"]
