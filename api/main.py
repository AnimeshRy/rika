"""Main entrypoint for the API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

app = FastAPI(lifespan=lifespan, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")

@app.get("/api/healthz")
def healthz():
    return "OK"

@app.exception_handler(NoResultFound)
async def not_found_error_handler(request: Request, exc: NoResultFound):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail": str(exc)}))


@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"detail": "API path Not Found"}))
