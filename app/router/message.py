from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.logger import log
from app.dependency import get_current_coach
from app.database import get_db
import app.model as m
import app.schema as s


message_router = APIRouter(prefix="/message", tags=["Messages"])


@message_router.post("/coach/send-message", response_model=s.Message)
def coach_create_message(
    message_data: s.MessageCreate,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    message = m.Message(
        message_from=coach.uuid,
        message_to=message_data.message_to,
        message_text=message_data.message_text,
    )
    db.add(message)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Error occured while creating message: %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occured while creating message",
        )
    log(log.INFO, "Message has been created successfully")
    return message


# get all messages with a specific user
@message_router.get("/coach/list-of-contacts", response_model=s.MessageUsersList)
def get_coach_list_of_contacts(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    messages: list[m.Message] = (
        db.query(m.Message).filter_by(message_from=coach.uuid).all()
    )
    result = list()
    for message in messages:
        student = db.query(m.Student).filter_by(uuid=message.message_to).first()
        result.append(student)
    return s.MessageUsersList(users=set(result))


# get messages for current dialogue
@message_router.get(
    "/coach/messages/{student_uuid}",
    response_model=s.MessageList,
)
def get_coach_student_messages(
    student_uuid: str,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    messages: list[m.Message] = (
        db.query(m.Message)
        .filter_by(message_from=coach.uuid, message_to=student_uuid)
        .order_by(m.Message.created_at.desc())
        .all()
    )

    return s.MessageList(messages=messages)
