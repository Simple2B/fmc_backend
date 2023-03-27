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
        db.query(m.Message).filter_by(receiver_id=student.uuid, is_read=False).count()
    )
    log(log.INFO, "Student has [%s] undread messages", new_messages_count)
    return s.MessageCount(count=new_messages_count)


@notifications_router.get("/coach/new", response_model=s.MessageCount)
def get_new_notifications_count_coach(
    db: Session = Depends(get_db), coach: m.Coach = Depends(get_current_coach)
):
    new_messages_count: int = (
        db.query(m.Message).filter_by(receiver_id=coach.uuid, is_read=False).count()
    )
    log(log.INFO, "Coach has [%s] undread messages", new_messages_count)
    return s.MessageCount(count=new_messages_count)
