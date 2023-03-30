from datetime import timedelta, datetime
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.logger import log
from app.dependency import (
    get_current_student,
)

from app.database import get_db
import app.model as m
import app.schema as s


notifications_router = APIRouter(prefix="/notification", tags=["Notification"])


@notifications_router.get("/student/reviews", response_model=s.UnreviewedLessonsList)
def get_review_notifications(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    # getting unreviewed lesson in range
    student_lessons = (
        db.query(m.StudentLesson)
        .filter(
            m.StudentLesson.student_id == student.id,
            m.StudentLesson.review_id == None,  # noqa:flake8 E711
            m.StudentLesson.appointment_time <= datetime.now() + timedelta(days=2),
        )
        .all()
    )
    log(log.INFO, "Lessons waiting for review - [%d]", len(student_lessons))
    return s.UnreviewedLessonsList(count=len(student_lessons), lessons=student_lessons)
