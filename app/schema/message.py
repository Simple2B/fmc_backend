from datetime import datetime
from pydantic import BaseModel

from .user.profile import User

import app.model as m


class MessageData(BaseModel):
    text: str
    receiver_id: str


class BaseMessage(BaseModel):
    uuid: str
    text: str | None
    created_at: datetime
    is_read: bool
    message_type: str | m.MessageType

    class Config:
        orm_mode = True


class Message(BaseMessage):
    author: User | None
    receiver: User

    class Config:
        orm_mode = True


class MessageList(BaseModel):
    messages: list[Message]


class Contact(BaseModel):
    user: User
    message: BaseMessage | None

    class Config:
        orm_mode = True


class ContactList(BaseModel):
    contacts: list[Contact]


class MessageCount(BaseModel):
    count: int


class ReviewMessage(BaseMessage):
    student: User
    coach: User
    created_at: datetime


class ReviewMessageList(BaseModel):
    messages: list[ReviewMessage]
