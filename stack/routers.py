from fastapi import APIRouter

from .models import Stack
from .schemas import StackCreate, StacksResponse
from .services import StackService

stack_router = APIRouter(tags=["stack"], prefix="/stack")


@stack_router.post("/")
async def create(stack_create: StackCreate) -> Stack:
    return await StackService().create(stack_create)


@stack_router.get("/id/{stack_id}")
async def get_by_id(stack_id: int) -> Stack:
    return await StackService().get_by_id(stack_id)


@stack_router.get("/all")
async def get_all() -> StacksResponse:
    return await StackService().get_all()
