from pydantic import BaseModel

from .models import User, Roles


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    role: Roles


class UserResponse(User.get_pydantic(exclude={"password_hash", "created_at"})):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserVerify(BaseModel):
    user_id: int
