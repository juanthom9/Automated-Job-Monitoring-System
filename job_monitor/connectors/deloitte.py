from dataclasses import replace

from connectors.avature import AvatureConnector
from connectors.successfactors import SuccessFactorsConnector
from models import Job


class DeloitteConnector:
    def __init__(self, company_name: str) -> None:
        self.company_name = company_name

    def fetch_jobs(self) -> list[Job]:
        sources = (
            (
                "us",
                AvatureConnector(
                    self.company_name,
                    "https://apply.deloitte.com/en_US/careers/SearchJobs/intern",
                    page_size=10,
                ),
            ),
            (
                "ca",
                SuccessFactorsConnector(
                    self.company_name,
                    "https://careers.deloitte.ca/",
                    locations=["Canada"],
                    search_query="intern",
                ),
            ),
        )

        jobs: list[Job] = []
        for source, connector in sources:
            jobs.extend(
                replace(job, external_id=f"{source}:{job.external_id}")
                for job in connector.fetch_jobs()
            )
        return jobs
