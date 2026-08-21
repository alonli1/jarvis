from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from ..models import LiteratureRecord


class LiteratureSource(ABC):
    name: str

    @abstractmethod
    def search(self, query: str, since: date, limit: int) -> list[LiteratureRecord]:
        raise NotImplementedError
