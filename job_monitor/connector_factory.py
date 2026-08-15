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
from connectors.intuit import IntuitConnector
from connectors.oracle_hcm import OracleHCMConnector
from connectors.phenom_widget import PhenomWidgetConnector
from connectors.ibm import IBMConnector
from connectors.successfactors import SuccessFactorsConnector
from connectors.jibe import JibeConnector
from connectors.shopify import ShopifyConnector
from connectors.adp_workforce_now import ADPWorkforceNowConnector
from connectors.paradox import ParadoxConnector
from connectors.avature import AvatureConnector
from connectors.plaid import PlaidConnector
from connectors.valve import ValveConnector
from connectors.deloitte import DeloitteConnector
from connectors.yello import YelloConnector
from connectors.kpmg import KPMGConnector
from connectors.confluent import ConfluentConnector
from connectors.mathworks import MathWorksConnector
from connectors.talentbrew import TalentBrewConnector
from connectors.jobsyn import JobSyncConnector

def create_connector(company: dict[str, Any]):
    # Read the connector name from companies.yaml
    connector_name = company["connector"].lower()

    if connector_name == "jobsyn":
        return JobSyncConnector(
            company_name=company["name"],
            origin=company["origin"],
        )

    if connector_name == "confluent":
        return ConfluentConnector(company_name=company["name"])

    if connector_name == "mathworks":
        return MathWorksConnector(company_name=company["name"])

    if connector_name == "talentbrew":
        return TalentBrewConnector(
            company_name=company["name"],
            search_url=company["search_url"],
            search_terms=company.get("search_terms"),
        )

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
            title_prefix=company.get("title_prefix"),
        )
    
    if connector_name == "greenhouse":
        return GreenhouseConnector(
            company_name=company["name"],
            board_token=company["board_token"],
            content_terms=company.get("content_terms"),
            location_aliases=company.get("location_aliases"),
        )
    
    if connector_name == "workday":
        return WorkdayConnector(
            company_name=company["name"],
            api_url=company["api_url"],
            public_base_url=company["public_base_url"],
            search_terms=company.get("search_terms"),
            additional_sites=company.get("additional_sites"),
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

    if connector_name == "intuit":
        return IntuitConnector(
            company_name=company["name"],
        )

    if connector_name == "oracle_hcm":
        return OracleHCMConnector(
            company_name=company["name"],
            api_base_url=company["api_base_url"],
            site_number=company["site_number"],
            site_path=company["site_path"],
        )

    if connector_name == "phenom_widget":
        return PhenomWidgetConnector(
            company_name=company["name"],
            widget_url=company["widget_url"],
            ref_num=company["ref_num"],
            locale=company.get("locale", "en_global"),
            country=company.get("country", "global"),
            search_term=company.get("search_term", "intern"),
            job_url_template=company.get("job_url_template"),
            company_names=company.get("company_names"),
            content_terms=company.get("content_terms"),
        )

    if connector_name == "ibm":
        return IBMConnector(
            company_name=company["name"],
            countries=company.get("countries"),
            experience_level=company.get("experience_level", "Internship"),
            search_query=company.get("search_query", ""),
        )

    if connector_name == "successfactors":
        return SuccessFactorsConnector(
            company_name=company["name"],
            base_url=company["base_url"],
            locations=company.get("locations"),
            search_query=company.get("search_query", "intern"),
        )

    if connector_name == "jibe":
        return JibeConnector(
            company_name=company["name"],
            api_url=company["api_url"],
            public_job_base_url=company["public_job_base_url"],
            include_description=company.get("include_description", True),
        )

    if connector_name == "shopify":
        return ShopifyConnector(company_name=company["name"])

    if connector_name == "adp_workforce_now":
        return ADPWorkforceNowConnector(
            company_name=company["name"],
            cid=company["cid"],
            cc_id=company["cc_id"],
            locale=company.get("locale", "en_US"),
        )

    if connector_name == "paradox":
        return ParadoxConnector(
            company_name=company["name"],
            base_url=company["base_url"],
            filter_key=company.get("filter_key"),
            filter_value=company.get("filter_value"),
        )

    if connector_name == "avature":
        return AvatureConnector(
            company_name=company["name"],
            search_url=company["search_url"],
        )

    if connector_name == "plaid":
        return PlaidConnector(company_name=company["name"])

    if connector_name == "valve":
        return ValveConnector(company_name=company["name"])

    if connector_name == "deloitte":
        return DeloitteConnector(company_name=company["name"])

    if connector_name == "yello":
        return YelloConnector(
            company_name=company["name"],
            board_id=company["board_id"],
            country_filter_ids=company["country_filter_ids"],
            search_query=company.get("search_query", "intern"),
        )

    if connector_name == "kpmg":
        return KPMGConnector(company_name=company["name"])

    if connector_name == "eightfold":
        return MicrosoftConnector(
            company_name=company["name"],
            domain=company["domain"],
            base_url=company["base_url"],
        )

    raise ValueError(
        f"Unsupported connector: {connector_name}"
    )
