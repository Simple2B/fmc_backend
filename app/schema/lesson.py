from pydantic import BaseModel, validator

from app.config import get_settings
from .location import Location
from .sport import SportType
from .user import Coach

settings = get_settings()


class BaseLesson(BaseModel):
    title: str | None
    location: Location
    sport: SportType
    price: int | float
    max_people: int | None
    about: str | None

    @validator("about")
    def validate_about(cls, value):
        if len(value) > 512:
            raise ValueError("About must be 512 characters long")
        return value

    @validator("price")
    def validate_price(cls, value):
        if isinstance(value, float):
            value = value * 100
        return value


class Lesson(BaseLesson):
    uuid: str
    id: int
    coach: Coach

    class Config:
        orm_mode = True


class LessonList(BaseModel):
    lessons: list[Lesson]
