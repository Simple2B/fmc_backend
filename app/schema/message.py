from datetime import datetime
from pydantic import BaseModel

from .user.profile import User


class MessageData(BaseModel):
    text: str
    receiver_id: str


class BaseMessage(BaseModel):
    uuid: str
    text: str
    created_at: datetime
    is_read: bool

    class Config:
        orm_mode = True


class Message(BaseMessage):
    author: User
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
