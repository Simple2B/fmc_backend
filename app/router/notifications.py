from datetime import datetime
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.logger import log
from app.dependency import (
    get_current_coach,
    get_current_student,
)

from app.database import get_db
import app.model as m
import app.schema as s


notifications_router = APIRouter(prefix="/notification", tags=["Notification"])


@notifications_router.get("/student/new", response_model=s.MessageCount)
def get_new_notifications_count_student(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    new_messages_count: int = (
        db.query(m.Message)
        .filter_by(
            receiver_id=student.uuid,
            is_read=False,
            message_type=m.MessageType.REVIEW_COACH,
        )
        .count()
    )
    log(log.INFO, "Student has [%s] undread messages", new_messages_count)
    return s.MessageCount(count=new_messages_count)


@notifications_router.post(
    "/student/reviews", response_model=s.ReviewMessageList
)  # for student
def get_review_notifications(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    # Give lessons without reviews !
    #
    #
    #
    #

    lessons = db.query(m.StudentLesson).filter_by(student_id=student.id).all()
    result = []
    for lesson in lessons:
        if lesson.appointment_time < datetime.now():  # TODO finish date logic
            result.append(lesson)
    review_notifications = [
        message
        for message in db.query(m.Message).filter_by(
            message_type=m.MessageType.REVIEW_COACH, is_read=False
        )
    ]
    for lesson in result:
        message = m.Message(
            message_type=m.MessageType.REVIEW_COACH, receiver_id=student.uuid
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        message = s.ReviewMessage(
            uuid=message.uuid,
            created_at=lesson.appointment_time,
            student=student,
            coach=lesson.coach,
            is_read=message.is_read,
            message_type=message.message_type,
        )
        if message not in review_notifications:
            review_notifications.append(message)

    return s.ReviewMessageList(messages=review_notifications)


@notifications_router.get("/coach/new", response_model=s.MessageCount)
def get_new_notifications_count_coach(
    db: Session = Depends(get_db), coach: m.Coach = Depends(get_current_coach)
):
    new_messages_count: int = (
        db.query(m.Message).filter_by(receiver_id=coach.uuid, is_read=False).count()
    )
    log(log.INFO, "Coach has [%s] undread messages", new_messages_count)
    return s.MessageCount(count=new_messages_count)
