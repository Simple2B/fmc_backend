from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from app.logger import log

from app.dependency import get_current_student, get_lesson_by_uuid
from app.database import get_db
import app.schema as s
import app.model as m

lesson_router = APIRouter(prefix="/lesson", tags=["Lesson"])


@lesson_router.get(
    "/lessons/upcoming",
    response_model=s.UpcomingLessonList,
    status_code=status.HTTP_200_OK,
)
def get_upcoming_lessons(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    upcoming_lessons = (
        db.query(m.StudentLesson)
        .filter(
            m.StudentLesson.student_id == student.id,
            m.StudentLesson.appointment_time >= datetime.now(),
        )
        .all()
    )
    log(log.INFO, "Total lessons found: %d", len(upcoming_lessons))
    return s.UpcomingLessonList(lessons=upcoming_lessons)


@lesson_router.get(
    "/{lesson_uuid}",
    response_model=s.StudentLesson,
    status_code=status.HTTP_200_OK,
)
def get_lesson(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
    lesson=Depends(get_lesson_by_uuid),
):
    return lesson
