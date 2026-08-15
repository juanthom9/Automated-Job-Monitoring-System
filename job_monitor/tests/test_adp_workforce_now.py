from connectors.adp_workforce_now import ADPWorkforceNowConnector


def test_map_job_maps_adp_requisition():
    connector = ADPWorkforceNowConnector(
        "ThinkOn",
        "tenant-id",
        "career-center-id",
        "en_CA",
    )
    posting = {
        "requisitionTitle": "Software Developer Intern",
        "postDate": "2026-08-12T15:25:00.000-04:00",
        "requisitionDescription": "Build cloud software.",
        "requisitionLocations": [
            {"nameCode": {"shortName": "Toronto, ON, CA"}}
        ],
    }

    job = connector._map_job(posting, "563717")

    assert job is not None
    assert job.external_id == "563717"
    assert job.location == "Toronto, ON, CA"
    assert job.description == "Build cloud software."
    assert "jobId=563717" in job.url
