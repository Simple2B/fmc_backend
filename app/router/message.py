from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.logger import log
from app.dependency import get_current_coach
from app.database import get_db
import app.model as m
import app.schema as s


message_router = APIRouter(prefix="/message", tags=["Messages"])


@message_router.post("/coach/send-message-to-student", response_model=s.MessageOut)
def coach_create_message(
    message_data: s.MessageDataIn,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    message: m.Message = m.Message(
        author_id=coach.uuid,
        receiver_id=message_data.receiver_id,
        text=message_data.text,
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
@message_router.get("/coach/list-of-contacts", response_model=s.BaseUserProfileList)
def get_coach_list_of_contacts(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    messages: list[m.Message] = (
        db.query(m.Message).filter_by(author_id=coach.uuid).all()
    )
    users = []
    for message in messages:
        student = db.query(m.Student).filter_by(uuid=message.receiver_id).first()
        users.append(student)
    return s.BaseUserProfileList(users=users)


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
        .filter_by(author_id=coach.uuid, receiver_id=student_uuid)
        .order_by(m.Message.created_at.desc())
        .all()
    )

    return s.MessageList(messages=messages)
