from datetime import datetime
from pydantic import BaseModel

from app.config import get_settings
from .user import Coach
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


class StudentLesson(BaseModel):
    coach: Coach
    lesson: Lesson
    appointment_time: datetime
    date: datetime

    class Config:
        orm_mode = True


class UpcomingLessonList(BaseModel):
    lessons: list[StudentLesson]
