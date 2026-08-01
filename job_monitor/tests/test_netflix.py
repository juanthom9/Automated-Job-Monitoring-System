import html
import json

from connectors.netflix import NetflixConnector


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


def test_fetch_jobs_maps_embedded_positions(monkeypatch):
    payload = {
        "positions": [
            {
                "id": 790313241540,
                "ats_job_id": "JR37687",
                "name": "Software Engineer PhD Intern",
                "location": "Los Gatos,California,United States of America",
                "canonicalPositionUrl": (
                    "https://explore.jobs.netflix.net/careers/job/790313241540"
                ),
                "job_description": "Work on streaming algorithms.",
            }
        ]
    }
    page = (
        '<code id="smartApplyData">'
        + html.escape(json.dumps(payload))
        + "</code>"
    )
    monkeypatch.setattr(
        "connectors.netflix.httpx.get",
        lambda *args, **kwargs: FakeResponse(page),
    )

    jobs = NetflixConnector("Netflix").fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "JR37687"
    assert jobs[0].company == "Netflix"
    assert jobs[0].title == "Software Engineer PhD Intern"
    assert jobs[0].location.startswith("Los Gatos")
