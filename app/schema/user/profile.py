from pydantic import BaseModel, AnyHttpUrl, validator

from .base import BaseUser
from ..sport import SportType
from ..certificate import Certificate
from ..location import Location
from app.config import get_settings, Settings

settings: Settings = get_settings()


class User(BaseUser):
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    profile_picture: AnyHttpUrl | None = settings.DEFAULT_AVATAR_URL
    # profile_picture: str | None

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[User]


class Coach(User):
    about: str = ""
    # TODO: must be check for frontend (this type AnyHttpUrl didn't work for frontend)
    is_for_adults: bool
    is_for_children: bool

    locations: list[Location]
    certificates: list[Certificate]
    sports: list[SportType] | None

    class Config:
        orm_mode = True

    @validator("about")
    def check_about_length(cls, v):
        if len(v) > 1024:
            raise ValueError("Length of 'about' couldnt be larger than 1024")
        return v


class Location(BaseUser):
    city: str
    street: str
    postal_code: str

    class Config:
        orm_mode = True


class Locations(BaseUser):
    locations: list[Location]
