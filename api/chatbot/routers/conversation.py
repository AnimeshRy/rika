from fastapi import APIRouter, HTTPException
from langchain_core.messages import BaseMessage, trim_messages
from sqlalchemy import select

from chatbot.dependancies import (
    SqlalchemyROSessionDep,
    SqlalchemySessionDep,
    UserIdHeaderDep,
)
from chatbot.models import Conversation as ORMConversation
from chatbot.schema import (
    ChatMessage,
    Conversation,
    ConversationDetail,
    CreateConversation,
    UpdateConversation,
)

router = APIRouter(
    prefix="/api/conversation",
    tags=["conversation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    userid: UserIdHeaderDep,
    session: SqlalchemyROSessionDep,
) -> "ConversationDetail":
    pass


@router.post("", status_code=201)
async def create_conversation(
    payload: CreateConversation, userid: UserIdHeaderDep, session: SqlalchemySessionDep
) -> "ConversationDetail":
    conv = ORMConversation(title=payload.title, owner=userid)
    session.add(conv)
    await session.commit()
    return conv


@router.put("/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    payload: UpdateConversation,
    userid: UserIdHeaderDep,
    session: SqlalchemySessionDep,
) -> "ConversationDetail":
    conv: ORMConversation = await session.get(ORMConversation, conversation_id)
    if conv.owner != userid:
        raise HTTPException(status_code=403, detail="authorization error")
    if payload.title is not None:
        conv.title = payload.title
    if payload.pinned is not None:
        conv.pinned = payload.pinned
    await session.commit()
    return conv


@router.get("/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: str, userid: UserIdHeaderDep, session: SqlalchemySessionDep
) -> None:
    conv: ORMConversation = await session.get(ORMConversation, conversation_id)
    if conv.owner != userid:
        raise HTTPException(status_code=403, detail="authorization error")
    await session.delete(conv)
    await session.commit()
