from connectors.microsoft import MicrosoftConnector


def test_custom_eightfold_tenant_configuration():
    connector = MicrosoftConnector(
        "Qualcomm",
        domain="qualcomm.com",
        base_url="https://careers.qualcomm.com/",
    )

    assert connector.domain == "qualcomm.com"
    assert connector.SEARCH_URL == (
        "https://careers.qualcomm.com/api/pcsx/search"
    )
