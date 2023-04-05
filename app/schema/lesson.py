from pydantic import BaseModel

from app.config import get_settings
from .location import Location
from .sport import SportType


settings = get_settings()


class Lesson(BaseModel):
    name: str
    location: Location
    sport: SportType
    price: float = settings.COACH_DEFAULT_LESSON_PRICE

    class Config:
        orm_mode = True


class LessonList(BaseModel):
    lessons: list[Lesson]
