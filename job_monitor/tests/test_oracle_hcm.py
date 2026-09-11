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


def test_paginates_when_api_caps_results_below_requested_size(monkeypatch):
    offsets = []

    def fake_get(*args, **kwargs):
        finder = kwargs["params"]["finder"]
        offset = int(finder.split("offset=", 1)[1].split(",", 1)[0])
        offsets.append(offset)
        ids = ["1", "2"] if offset == 0 else ["3"]
        return FakeResponse({
            "items": [{
                "TotalJobsCount": 3 if offset == 0 else 0,
                "requisitionList": [
                    {
                        "Id": job_id,
                        "Title": f"Software Intern {job_id}",
                        "PrimaryLocation": "Toronto, Canada",
                    }
                    for job_id in ids
                ],
            }],
        })

    monkeypatch.setattr("connectors.oracle_hcm.httpx.get", fake_get)
    jobs = OracleHCMConnector(
        "Oracle",
        "https://example.oraclecloud.com",
        "CX_1",
        "jobsearch",
    ).fetch_jobs()

    assert offsets == [0, 2]
    assert [job.external_id for job in jobs] == ["1", "2", "3"]
