from datetime import datetime
from pydantic import BaseModel

from .user.profile import BaseUserProfileOut


class MessageDataIn(BaseModel):
    text: str
    receiver_id: str  # User # creation form


class MessageOut(BaseModel):
    author: BaseUserProfileOut
    receiver: BaseUserProfileOut
    text: str
    created_at: datetime
    is_read: bool

    class Config:
        orm_mode = True


class MessageList(BaseModel):
    messages: list[MessageOut]

    class Config:
        orm_mode = True
