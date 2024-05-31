from typing import List, Set

from pydantic import BaseModel
from .models import ResumeModel


class SearchRequest(BaseModel):
    stack: List[str] = None
    limit: int = 20
    skip: int = 0
    experience_from: int | None = 0
    experience_to: int | None = 100


class SearchResume(ResumeModel):
    percent: float = None


class SearchResponse(BaseModel):
    result: List[SearchResume]
