from pydantic import BaseModel, validator

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
    profile_picture: str | None = ""

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[User]


class Coach(User):
    about: str = ""
    is_for_adults: bool
    is_for_children: bool
    about: str | None

    locations: list[Location] | None
    certificates: list[Certificate] | None
    sports: list[SportType] | None

    class Config:
        orm_mode = True

    @validator("about")
    def check_about_length(cls, v):
        if len(v) > 1024:
            raise ValueError("Length of 'about' couldn't be larger than 1024")
        return v


class FavouriteCoach(Coach):
    is_favourite: bool

    class Config:
        orm_mode = True


class CoachList(BaseModel):
    coaches: list[Coach]


class FavoriteCoachList(BaseModel):
    coaches: list[FavouriteCoach]
