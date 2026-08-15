from connectors.phenom_widget import PhenomWidgetConnector


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "refineSearch": {
                "totalHits": 1,
                "data": {
                    "jobs": [
                        {
                            "reqId": "123",
                            "title": "Software Engineer Intern",
                            "applyUrl": "https://example.com/job/123",
                            "location": "Toronto, Ontario, Canada",
                            "descriptionTeaser": "Build software.",
                        }
                    ]
                },
            }
        }


def test_fetch_jobs_maps_widget_results(monkeypatch):
    monkeypatch.setattr(
        "connectors.phenom_widget.httpx.post",
        lambda *args, **kwargs: FakeResponse(),
    )
    jobs = PhenomWidgetConnector(
        "Cisco",
        "https://example.com/widgets",
        "EXAMPLE",
    ).fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "123"
    assert jobs[0].title == "Software Engineer Intern"
    assert jobs[0].location == "Toronto, Ontario, Canada"


def test_fetch_jobs_builds_url_when_feed_omits_apply_url(monkeypatch):
    class ResponseWithoutApplyUrl(FakeResponse):
        def json(self):
            data = super().json()
            del data["refineSearch"]["data"]["jobs"][0]["applyUrl"]
            return data

    monkeypatch.setattr(
        "connectors.phenom_widget.httpx.post",
        lambda *args, **kwargs: ResponseWithoutApplyUrl(),
    )
    jobs = PhenomWidgetConnector(
        "Bell",
        "https://example.com/widgets",
        "EXAMPLE",
        job_url_template="https://example.com/job/{job_id}",
    ).fetch_jobs()

    assert jobs[0].url == "https://example.com/job/123"
