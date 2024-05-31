from .exceptions import StackNotFound, StackAlreadyExist
from .models import Stack
from .repositories import StackRepository
from .schemas import StackCreate
from config import DEFAULT_STACKS


class StackService:
    repository = StackRepository()

    async def create(self, stack_create: StackCreate) -> Stack:
        if await self.repository.get_by_title(stack_create.title) is not None:
            raise StackAlreadyExist
        return await self.repository.create(stack_create)

    async def get_by_id(self, stack_id: int) -> Stack:
        stack =  await self.repository.get_by_id(stack_id)
        if stack is None:
            raise StackNotFound
        return stack

    async def get_by_title(self, stack_title: int) -> Stack:
        return await self.repository.get_by_title(stack_title)

    async def get_all(self):
        return await self.repository.get_all()

    async def init_default_stack(self):
        for s in DEFAULT_STACKS:
            if (await self.repository.get_by_title(s)) is None:
                await self.repository.create(StackCreate(title=s))
