from datetime import datetime
from pydantic import BaseModel


from .user import User, Coach
from .schedule import Schedule


class StudentLesson(BaseModel):
    uuid: str
    student_id: int
    schedule_id: int
    coach_id: int

    student: User
    schedule: Schedule
    coach: Coach
    appointment_time: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class UpcomingLessonList(BaseModel):
    lessons: list[StudentLesson]


class UnreviewedLessonsList(BaseModel):
    count: int
    lessons: list[StudentLesson]
