from copy import deepcopy
from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, ConfigDict, Field, field_validator

from chatbot.utils import utcnow


class UserProfile(BaseModel):
    userid: str
    username: str | None = None
    email: str | None = None


class ChatMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parent_id: str | None = None
    id: str = Field(default_factory=lambda: str(uuid4()))
    conversation: str | None = None
    from_: str | None = Field(None, alias="from")
    content: str | list[str | dict] | None = None
    type: Literal[
        "text", "stream/start", "stream/text", "stream/end", "info", "error"
    ] = "text"
    feedback: Literal["thumbsup", "thumbsdown", None] = None
    additional_kwargs: dict[str, Any] | None = None

    @staticmethod
    def from_lc(
        lc_message: BaseMessage, conv_id: str, from_: str = None
    ) -> "ChatMessage":
        additional_kwargs = deepcopy(lc_message.additional_kwargs)
        return ChatMessage(
            parent_id=additional_kwargs.pop("parent_id", None),
            id=lc_message.id or str(uuid4()),
            conversation=conv_id or additional_kwargs.pop("session_id", None),
            from_=from_ or lc_message.type,
            content=lc_message.content,
            type=additional_kwargs.pop("type", "text"),
            feedback=additional_kwargs.pop("feedback", None),
            additional_kwargs=additional_kwargs,
        )


class Conversation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | UUID | None = None
    title: str
    owner: str
    pinned: bool = False
    created_at: datetime = Field(default_factory=utcnow)
    last_message_at: datetime = created_at

    @field_validator("id")
    @classmethod
    def convert_id(cls, v: UUID) -> str:
        return str(v)


class ConversationDetail(Conversation):
    """Conversation with messages"""

    messages: list[ChatMessage] = []


class CreateConversation(BaseModel):
    title: str


class UpdateConversation(BaseModel):
    title: str | None = None
    pinned: bool | None = None


class Share(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | UUID | None = None
    title: str
    url: str
    owner: str
    messages: list[ChatMessage] = []
    created_at: datetime = Field(default_factory=utcnow)

    @field_validator("id")
    @classmethod
    def convert_id(cls, v: UUID) -> str:
        return str(v)


class CreateShare(BaseModel):
    title: str
    source_id: str
