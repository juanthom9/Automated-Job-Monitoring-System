from typing import Any

from connectors.ashby import AshbyConnector
from connectors.lever import LeverConnector
from connectors.greenhouse import GreenhouseConnector
from connectors.workday import WorkdayConnector
from connectors.smartrecruiters import SmartRecruitersConnector
from connectors.phenom import PhenomConnector
from connectors.amazon import AmazonConnector
from connectors.apple import AppleConnector
from connectors.google import GoogleConnector
from connectors.netflix import NetflixConnector
from connectors.microsoft import MicrosoftConnector

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
            search_terms=company.get("search_terms"),
        )

    if connector_name == "smartrecruiters":
        return SmartRecruitersConnector(
            company_name=company["name"],
            company_identifier=company["company_identifier"],
        )

    if connector_name == "phenom":
        return PhenomConnector(
            company_name=company["name"],
            api_url=company["api_url"],
            query_params=company.get("query_params"),
        )

    if connector_name == "amazon":
        return AmazonConnector(
            company_name=company["name"],
            search_query=company.get("search_query", "intern"),
        )

    if connector_name == "apple":
        return AppleConnector(
            company_name=company["name"],
        )

    if connector_name == "google":
        return GoogleConnector(
            company_name=company["name"],
        )

    if connector_name == "netflix":
        return NetflixConnector(
            company_name=company["name"],
        )

    if connector_name == "microsoft":
        return MicrosoftConnector(
            company_name=company["name"],
        )

    if connector_name == "eightfold":
        return MicrosoftConnector(
            company_name=company["name"],
            domain=company["domain"],
            base_url=company["base_url"],
        )

    raise ValueError(
        f"Unsupported connector: {connector_name}"
    )
