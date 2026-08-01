from connectors.amazon import AmazonConnector


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


def test_fetch_jobs_maps_amazon_record(monkeypatch):
    payload = {
        "hits": 1,
        "jobs": [
            {
                "id_icims": "12345",
                "title": "Software Development Intern",
                "job_path": "/en/jobs/12345/software-development-intern",
                "normalized_location": "Toronto, Ontario, CAN",
                "description": "Build software.",
            }
        ],
    }
    monkeypatch.setattr(
        "connectors.amazon.httpx.get",
        lambda *args, **kwargs: FakeResponse(payload),
    )

    jobs = AmazonConnector("Amazon").fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "12345"
    assert jobs[0].location == "Toronto, Ontario, CAN"
    assert jobs[0].url == (
        "https://www.amazon.jobs/en/jobs/12345/"
        "software-development-intern"
    )
