from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph.graph import CompiledGraph
from sqlalchemy.ext.asyncio import AsyncSession

from chatbot.state import sqlalchemy_ro_session, sqlalchemy_session


def UserIdHeader(alias: str | None = None, **kwargs):
    if alias is None:
        alias = "X-Forwarded-User"
    return Header(alias=alias, **kwargs)


UserIdHeaderDep = Annotated[str | None, UserIdHeader()]


async def get_alchemy_ro_session() -> AsyncGenerator[AsyncSession, None]:
    async with sqlalchemy_ro_session() as session:
        yield session


SqlalchemyROSessionDep = Annotated[AsyncSession, Depends(get_alchemy_ro_session)]


async def get_alchemy_session() -> AsyncGenerator[AsyncSession, None]:
    async with sqlalchemy_session() as session:
        yield session


SqlalchemySessionDep = Annotated[AsyncSession, Depends(get_alchemy_session)]
