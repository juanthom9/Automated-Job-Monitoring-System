from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    # Basic job information
    external_id: str
    company: str
    title: str
    url: str

    # Optional job details
    location: str | None = None
    description: str | None = None
    posted_at: datetime | None = None