from coverage import build_coverage_report, classify_company


def test_classify_company_states():
    assert classify_company(
        {
            "connector": "greenhouse",
            "enabled": True,
            "validation_status": "valid",
        }
    ) == "validated"
    assert classify_company(
        {"connector": "workday", "enabled": True}
    ) == "configured_unvalidated"
    assert classify_company(
        {"connector": "unresolved", "enabled": False}
    ) == "needs_investigation"
    assert classify_company(
        {"connector": "unsupported", "enabled": False}
    ) == "needs_connector"


def test_report_contains_summary_and_company():
    report = build_coverage_report(
        [
            {
                "name": "Example",
                "careers_url": "https://example.com/jobs",
                "connector": "lever",
                "enabled": True,
            }
        ]
    )

    assert "Total companies: **1**" in report
    assert "configured_unvalidated | 1" in report
    assert "| Example |" in report
