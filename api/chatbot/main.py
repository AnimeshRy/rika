"""Main entrypoint for the API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from prometheus_client import make_asgi_app
from sqlalchemy.exc import NoResultFound

from chatbot.config import settings
from chatbot.models import Base
from chatbot.state import sqlalchemy_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create table or ORM models
    async with sqlalchemy_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create checkpointer tables
    async with AsyncPostgresSaver.from_conn_string(
        settings.psycopg_primary_url
    ) as checkpointer:
        await checkpointer.setup()

    yield


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# TODO: Add Routes below


@app.get("/api/healthz")
def healthz():
    return "OK"


@app.get("/api/userinfo")
def userinfo():
    return {"userid": "animesh", "username": "animesh", "email": "animesh@gmail.com"}


@app.exception_handler(NoResultFound)
async def not_found_error_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"detail": str(exc)}),
    )


@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder({"detail": "API path Not Found"}),
        )
