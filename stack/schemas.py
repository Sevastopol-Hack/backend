from typing import List

from pydantic import BaseModel

from .models import Stack


class StackCreate(BaseModel):
    title: str


StacksResponse = List[Stack]
