import databases
import ormar
import sqlalchemy
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import TEXT

from config import DATABASE_URL, MONGODB_URL
from pydantic import BaseModel, ConfigDict
from bson import ObjectId

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


mongo_client = AsyncIOMotorClient(MONGODB_URL)

mongo_db = mongo_client["biworking"]


class BaseModelWithConfig:
    validate_assignment = True
    from_attributes = True
    populate_by_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


async def create_index():
    await mongo_db.Resumes.create_index([('stack', TEXT), ])
    await mongo_db.Vacancy.create_index([('title', TEXT), ])
