from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from app.logger import log

from app.dependency import get_current_student, get_lesson_by_uuid, get_current_coach
from app.database import get_db
import app.schema as s
import app.model as m

lesson_router = APIRouter(prefix="/lesson", tags=["Lesson"])


@lesson_router.get(
    "/lessons/student",
    response_model=list[s.StudentLesson],
    status_code=status.HTTP_200_OK,
)
def get_lessons_for_student(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    upcoming_lessons = (
        db.query(m.StudentLesson)
        .filter(
            m.StudentLesson.student_id == student.id,
        )
        .all()
    )
    log(log.INFO, "Total lessons found: %d", len(upcoming_lessons))
    return [s.StudentLesson.from_orm(lesson) for lesson in upcoming_lessons]


@lesson_router.get(
    "/lessons/student/upcoming",
    response_model=s.StudentLessonList,
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
    return s.StudentLessonList(lessons=upcoming_lessons)


@lesson_router.get(
    "/lessons/coach/upcoming",
    response_model=s.StudentLessonList,
    status_code=status.HTTP_200_OK,
)
def get_upcoming_appointments(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    upcoming_lessons = (
        db.query(m.StudentLesson)
        .join(m.CoachSchedule)
        .filter_by(coach_id=coach.id)
        .filter(
            m.StudentLesson.appointment_time >= datetime.now(),
        )
        .all()
    )
    log(log.INFO, "Total appointments found: %d", len(upcoming_lessons))
    return s.StudentLessonList(lessons=upcoming_lessons)


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
