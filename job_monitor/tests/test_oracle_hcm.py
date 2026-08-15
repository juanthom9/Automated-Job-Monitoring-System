from connectors.oracle_hcm import OracleHCMConnector


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_fetch_jobs_maps_and_deduplicates_requisitions(monkeypatch):
    payload = {
        "items": [
            {
                "TotalJobsCount": 1,
                "requisitionList": [
                    {
                        "Id": "12345",
                        "Title": "Software Engineering Intern",
                        "PrimaryLocation": "Toronto, ON, Canada",
                        "PostedDate": "2026-08-01",
                        "ShortDescriptionStr": "Build cloud services.",
                    }
                ],
            }
        ]
    }
    monkeypatch.setattr(
        "connectors.oracle_hcm.httpx.get",
        lambda *args, **kwargs: FakeResponse(payload),
    )

    jobs = OracleHCMConnector(
        "Oracle",
        "https://example.oraclecloud.com",
        "CX_1",
        "jobsearch",
    ).fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "12345"
    assert jobs[0].title == "Software Engineering Intern"
    assert jobs[0].location == "Toronto, ON, Canada"
    assert jobs[0].posted_at.isoformat() == "2026-08-01T00:00:00"
    assert jobs[0].url.endswith("/sites/jobsearch/job/12345")

