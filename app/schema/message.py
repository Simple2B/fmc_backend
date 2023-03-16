from datetime import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    message_text: str
    message_to: str


class Message(BaseModel):
    message_from: str
    message_to: str
    message_text: str
    created_at: datetime

    class Config:
        orm_mode = True


class MesssageUser(BaseModel):
    email: str
    uuid: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class MessageUsersList(BaseModel):
    users: list[MesssageUser]

    class Config:
        orm_mode = True


class MessageList(BaseModel):
    messages: list[Message]

    class Config:
        orm_mode = True
