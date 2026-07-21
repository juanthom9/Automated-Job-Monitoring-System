from typing import Any

from connectors.ashby import AshbyConnector
from connectors.lever import LeverConnector
from connectors.greenhouse import GreenhouseConnector
from connectors.workday import WorkdayConnector

def create_connector(company: dict[str, Any]):
    # Read the connector name from companies.yaml
    connector_name = company["connector"].lower()

    if connector_name == "ashby":
        return AshbyConnector(
            company_name=company["name"],
            board_name=company["board_name"],
        )

    if connector_name == "lever":
        return LeverConnector(
            company_name=company["name"],
            site_name=company["site_name"],
            region=company.get("region", "global"),
        )
    
    if connector_name == "greenhouse":
        return GreenhouseConnector(
            company_name=company["name"],
            board_token=company["board_token"],
        )
    
    if connector_name == "workday":
        return WorkdayConnector(
            company_name=company["name"],
            api_url=company["api_url"],
            public_base_url=company["public_base_url"],
        )

    raise ValueError(
        f"Unsupported connector: {connector_name}"
    )