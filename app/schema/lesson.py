from pydantic import BaseModel

from .user import Coach
from .location import Location
from .sport import SportTypeSchema


class Lesson(BaseModel):
    location: Location
    sport: SportTypeSchema

    class Config:
        orm_mode = True


class LessonList(BaseModel):
    lessons: list[Lesson]


class StudentLesson(BaseModel):
    coach: Coach
    lesson: Lesson

    class Config:
        orm_mode = True


class UpcomingLessonList(BaseModel):
    lessons: list[StudentLesson]
