from typing import List

from pydantic import BaseModel
from .models import VacancyModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 20
    skip: int = 0


class SearchResponse(BaseModel):
    result: List[dict]
