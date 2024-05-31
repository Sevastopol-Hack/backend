from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import BUCKET_NAME, LOGGING_CONFIG, METRICS, PRODUCTION
from database import database, create_index
from resume.routers import resume_router
from s3.api import S3Worker
from stack.routers import stack_router
from stack.services import StackService
from users.routers import user_router
from utils import apply_migrations
from vacancy.routers import vacancy_router
from yagpt.routers import yagpt_router

logger = getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_migrations()

    await S3Worker.new_bucket(BUCKET_NAME, ignore_existing=True)
    await create_index()

    database_ = app.state.database

    if not database_.is_connected:
        await database_.connect()

    await StackService().init_default_stack()


    yield

    # shutdown

    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app = FastAPI(lifespan=lifespan, title="biwork api")
app.state.database = database

if METRICS:
    from prometheus_fastapi_instrumentator import Instrumentator

    Instrumentator().instrument(app).expose(app)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/{url}")
async def handle_options(url):
    return JSONResponse({"ok": True}, headers={"Access-Control-Allow-Headers": "*"})


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, err) -> JSONResponse:
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=500,
        content={"message": f"{base_error_message}. Detail: {str(err)}"},
    )


@app.get("/ping")
async def ping_pong():
    return "pong"


app.include_router(user_router)
app.include_router(yagpt_router)
app.include_router(resume_router)
app.include_router(vacancy_router)
app.include_router(stack_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=80,
        host="0.0.0.0",
        reload=not PRODUCTION,
        log_config=LOGGING_CONFIG,
    )
