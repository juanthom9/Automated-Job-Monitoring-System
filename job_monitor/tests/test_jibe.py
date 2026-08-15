from connectors.jibe import JibeConnector


def test_map_job_maps_jibe_posting():
    connector = JibeConnector(
        "Example",
        "https://careers.example.com/api/jobs",
        "https://careers.example.com/jobs",
    )

    job = connector._map_job(
        {
            "data": {
                "req_id": "1234",
                "title": "Software Engineering Intern",
                "language": "en-us",
                "full_location": "Canada; Ontario, Canada",
                "description": "Build developer tools.",
                "posted_date": "2026-08-14T20:10:00+0000",
            }
        }
    )

    assert job is not None
    assert job.external_id == "1234"
    assert job.location == "Canada; Ontario, Canada"
    assert job.url == "https://careers.example.com/jobs/1234?lang=en-us"
    assert job.posted_at.isoformat() == "2026-08-14T20:10:00+00:00"
