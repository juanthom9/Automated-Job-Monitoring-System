from connectors.shopify import ShopifyConnector


def test_map_job_maps_shopify_posting():
    job = ShopifyConnector("Shopify")._map_job(
        {
            "jobPosting": {
                "id": "posting-123",
                "title": "Software Engineering Intern",
                "locationName": "Canada",
                "workplaceType": "Remote",
                "publishedDate": "2026-08-01",
                "externalLink": (
                    "https://www.shopify.com/careers?ashby_jid=posting-123"
                ),
            }
        }
    )

    assert job is not None
    assert job.external_id == "posting-123"
    assert job.location == "Remote - Canada"
    assert job.posted_at.isoformat() == "2026-08-01T00:00:00"
