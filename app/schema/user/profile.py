from pydantic import BaseModel, AnyHttpUrl, validator
from .base import BaseUser


class User(BaseUser):
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    profile_picture: AnyHttpUrl | None

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[User]


class Coach(User):
    about: str = ""
    certificate_url: AnyHttpUrl | None
    is_for_adults: bool
    is_for_children: bool

    class Config:
        orm_mode = True

    @validator("about")
    def check_about_length(cls, v):
        if len(v) > 1024:
            raise ValueError("Length of 'about' couldnt be larger than 1024")
        return v
