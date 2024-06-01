from typing import Optional

from .models import Stack
from .schemas import StackCreate


class StackRepository:
    async def create(self, stack_create: StackCreate) -> Stack:
        stack = Stack(**stack_create.dict())
        await stack.save()

        return stack

    async def get_by_id(self, stack_id: int) -> Optional[Stack]:
        return await Stack.objects.get_or_none(id=stack_id)

    async def get_by_title(self, stack_title):
        return await Stack.objects.get_or_none(title=stack_title)

    async def get_all(self):
        res = await Stack.objects.all()
        return res
