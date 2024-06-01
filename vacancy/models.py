from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field
from pydantic import Field as PydanticField
from pydantic import validator

from utils.mongodb import PyObjectId, get_current_time_in_unix_format


class VacancyModel(BaseModel):
    id: Optional[PyObjectId] = PydanticField(default_factory=PyObjectId, alias="_id")
    created_at: Optional[float] = Field(default=None, validate_default=True)

    title: str
    stack: List[str]
    is_close: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: lambda oid: str(oid)}

    @validator("created_at")
    @classmethod
    def init_create_and_update_time(cls, v: float) -> float:
        """
        The creation and update time is set once
        """
        return v or get_current_time_in_unix_format()
