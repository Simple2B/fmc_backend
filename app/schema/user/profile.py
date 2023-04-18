from pydantic import BaseModel, validator

from .base import BaseUser
from ..sport import SportType
from ..certificate import Certificate
from ..location import Location
from ..review import Review
from app.config import get_settings, Settings

settings: Settings = get_settings()


class User(BaseUser):
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    profile_picture: str | None = ""
    stripe_account_id: str | None

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[User]


class Coach(User):
    total_rate: float
    about: str = ""
    experience: str | None
    credentials: str | None
    is_for_adults: bool
    is_for_children: bool
    about: str | None

    locations: list[Location]
    certificates: list[Certificate]
    sports: list[SportType]
    reviews: list[Review]

    class Config:
        orm_mode = True

    @validator("about")
    def check_about_length(cls, v):
        if len(v) > 1024:
            raise ValueError("Length of 'about' couldn't be larger than 1024")
        return v


class CoachList(BaseModel):
    coaches: list[Coach]
