from typing import Optional, List

from pydantic import Field
from pydantic import validator

from utils.mongodb import get_current_time_in_unix_format, PyObjectId

from pydantic import BaseModel, Field as PydanticField
from bson import ObjectId


class Job(BaseModel):
    name: str = ""
    post: str = ""
    start: int = 0
    end: int = None


class ResumeModel(BaseModel):
    id: Optional[PyObjectId] = PydanticField(default_factory=PyObjectId, alias="_id")
    created_at: Optional[float] = Field(default=None, validate_default=True)
    fio: str = ""
    age: int = 0
    experience: int = 0
    stack: List[str] = []
    jobs: list[Job] = []
    filename: str = None
    email: str = ""

    def getId(self):
        return self.id

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: lambda oid: str(oid)
                         }

    @validator("created_at", )
    @classmethod
    def init_create_and_update_time(cls, v: float) -> float:
        """
        The creation and update time is set once
        """
        return v or get_current_time_in_unix_format()


class UploadedResume(BaseModel):
    id: Optional[PyObjectId] = PydanticField(default_factory=PyObjectId, alias="_id")
    created_at: Optional[float] = Field(default=None, validate_default=True)
    user_id: int
    resumes: List[str]

    def getId(self):
        return self.id

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: lambda oid: str(oid)}
