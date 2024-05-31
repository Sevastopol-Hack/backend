from typing import Annotated, List

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from config import ALGORITHM, SECRET_KEY
from utils.passwords import verify_password

from .models import User
from .repositories import UserRepository
from .schemas import TokenData, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserService:
    repository = UserRepository()

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.repository.get_by_username(username)
        if not user:
            return
        if not verify_password(password, user.password_hash):
            return
        return user

    async def authenticate_user_by_token(self, token: str) -> User | None:
        pass

    async def get_current_user(self,
                               token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token = token.strip()
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except jwt.DecodeError:
            raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise credentials_exception
        user = await self.repository.get_by_id(int(token_data.user_id))
        if user is None:
            raise credentials_exception
        return user

    async def create(self, user_create: UserCreate) -> User:
        return await self.repository.create(user_create)

    async def add_unused_votes(self, user_id: int, votes: int):
        return await self.repository.add_unused_votes(user_id, votes)

    async def subtract_user_voice(self, user: User, amount: int) -> None:
        await self.repository.subtract_user_voice(user, amount)

    async def delete_user(self, user: User) -> None:
        await self.repository.delete_user(user)

    async def verify_user(self, user_id: int) -> None:
        user = await self.repository.get_by_id(user_id)
        user.is_verified = True
        await user.update()

    async def get_all_users(self, offset: int = 0, limit: int = 20):
        res = await self.repository.get_all_users(offset, limit)
        print(res)
        return res
