from datetime import datetime

import time
from typing import NoReturn, Annotated

from bson import ObjectId

from database import BaseModelWithConfig
from utils.exeptions import DocumentNotFound, InvalidObjectId
from bson.objectid import ObjectId as BsonObjectId


def get_current_time_in_unix_format() -> float:
    """
    Get time in Unix
    """
    return time.mktime(datetime.now().timetuple())


async def is_document_found(
        my_object: BaseModelWithConfig | None,
) -> BaseModelWithConfig | None:
    """
    Checking that Document is found
    """
    if not my_object:
        raise DocumentNotFound()
    return my_object


async def is_valid_object_id(object_id: str) -> NoReturn:
    """
    Checking that ObjectId is valid
    """
    if not ObjectId.is_valid(object_id):
        raise InvalidObjectId(object_id)


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    @classmethod
    def modify_schema(cls, field_schema):
        field_schema.update(type="string")
