from pydantic import BaseModel, AnyHttpUrl
from .base import BaseUser


class BaseUserProfileOut(BaseUser):
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    profile_picture: AnyHttpUrl

    class Config:
        orm_mode = True


class BaseUserProfileList(BaseModel):
    users: list[BaseUserProfileOut]

    class Config:
        orm_mode = True
