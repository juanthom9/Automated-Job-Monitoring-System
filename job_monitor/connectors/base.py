from __future__ import annotations

from abc import ABC, abstractmethod

import httpx

from ..models import Company, Job


class Connector(ABC):
    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    @abstractmethod
    def fetch(self, company: Company) -> list[Job]:
        raise NotImplementedError
