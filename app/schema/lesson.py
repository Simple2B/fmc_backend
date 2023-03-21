from pydantic import BaseModel

from .user import Coach


class Lesson(BaseModel):
    ...

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
