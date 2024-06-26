from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from utils.passwords import get_password_hash

from .models import Roles, User
from .schemas import UserCreate, UserResponse


class UserRepository:
    """
    UserRepository
    """

    async def create(self, user_create: UserCreate) -> User:
        if await User.objects.get_or_none(username=user_create.username):
            raise HTTPException(
                status_code=400, detail="User with this username already exists"
            )
        password = user_create.password

        dc = user_create.dict(exclude={"password"})
        dc["password_hash"] = get_password_hash(password)
        dc["role"] = user_create.role

        user = User(**dc)
        await user.save()

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        return await User.objects.get_or_none(email=email)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await User.objects.get_or_none(username=username)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await User.objects.get_or_none(id=user_id)

    async def add_unused_votes(self, user_id: int, votes: int) -> User:
        user = await User.objects.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.unused_votes += votes
        await user.update()
        return user

    async def subtract_user_voice(self, user: User, amount) -> None:
        await user.update(unused_votes=user.unused_votes - amount)

    async def delete_user(self, user: User) -> None:
        await user.delete()

    async def count(self) -> int:
        return await User.objects.count()

    async def get_all_users(self, offset: int = 0, limit: int = 20) -> List[User]:
        return await User.objects.limit(limit).offset(offset).all()
