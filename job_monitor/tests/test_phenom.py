from connectors.phenom import PhenomConnector


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


def test_fetch_jobs_maps_nested_phenom_data(monkeypatch):
    payload = {
        "totalCount": 1,
        "jobs": [
            {
                "data": {
                    "req_id": "123",
                    "title": "Software Engineering Intern",
                    "full_location": "Markham, Ontario",
                    "description": "Build software.",
                    "apply_url": "https://apply.example/123",
                    "meta_data": {
                        "canonical_url": "https://careers.example/jobs/123"
                    },
                }
            }
        ],
    }
    monkeypatch.setattr(
        "connectors.phenom.httpx.get",
        lambda *args, **kwargs: FakeResponse(payload),
    )

    connector = PhenomConnector(
        "Example",
        "https://careers.example/api/jobs",
        {"categories": "Student / Intern / Temp"},
    )
    jobs = connector.fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "123"
    assert jobs[0].location == "Markham, Ontario"
    assert jobs[0].url == "https://careers.example/jobs/123"
