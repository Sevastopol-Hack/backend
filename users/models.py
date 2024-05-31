import datetime
from enum import Enum

import ormar

from database import BaseMeta


class Roles(Enum):
    admin = "admin"
    recruiter = "recruiter"
    hiring_manager = "hiring_manager"
    resource_manager = "resource_manager"


class Gender(Enum):
    male = "male"
    female = "female"


class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    surname: str = ormar.String(max_length=200)
    username: str = ormar.String(max_length=200)
    is_verified: bool = ormar.Boolean(default=False)
    role: Roles = ormar.Enum(enum_class=Roles)
    password_hash: str = ormar.String(max_length=200)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
