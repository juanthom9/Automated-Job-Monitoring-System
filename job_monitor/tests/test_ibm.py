from connectors.ibm import IBMConnector


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "hits": {
                "hits": [
                    {
                        "_id": "ibm-123",
                        "_source": {
                            "title": "Software Developer Intern",
                            "url": "https://careers.ibm.com/careers/JobDetail?jobId=123",
                            "field_keyword_19": "Toronto, CA",
                            "description": "Build cloud software.",
                        },
                    }
                ]
            }
        }


def test_fetch_jobs_maps_public_search_results(monkeypatch):
    captured = {}

    def fake_post(*args, **kwargs):
        captured.update(kwargs["json"])
        return FakeResponse()

    monkeypatch.setattr("connectors.ibm.httpx.post", fake_post)

    jobs = IBMConnector("IBM").fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0].external_id == "ibm-123"
    assert jobs[0].title == "Software Developer Intern"
    assert jobs[0].location == "Toronto, CA"
    assert captured["appId"] == "careers"
    assert captured["scopes"] == ["careers2"]
    assert captured["post_filter"]["bool"]["must"][1] == {
        "term": {"field_keyword_18": "Internship"}
    }


def test_payload_supports_company_keyword() -> None:
    payload = IBMConnector("HashiCorp", search_query="hashicorp")._payload(0)

    assert payload["query"]["bool"]["must"] == [
        {
            "multi_match": {
                "query": "hashicorp",
                "fields": ["title^3", "description"],
            }
        }
    ]
    assert payload["sm"]["query"] == "hashicorp"
