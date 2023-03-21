from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.logger import log
from app.dependency import (
    get_current_coach,
    get_current_student,
    get_student_by_uuid,
    get_coach_by_uuid,
)
from app.database import get_db
import app.model as m
import app.schema as s


message_router = APIRouter(prefix="/message", tags=["Messages"])


@message_router.post("/coach/create", response_model=s.Message)
def coach_create_message(
    message_data: s.MessageData,
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
@message_router.get("/coach/list-of-contacts", response_model=s.UserList)
def get_coach_list_of_contacts(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    # messages where coach is owner
    messages: list[m.Message] = (
        db.query(m.Message).filter_by(author_id=coach.uuid).all()
    )
    contacts: list = []
    for message in messages:
        student = db.query(m.Student).filter_by(uuid=message.receiver_id).first()
        contacts.append(student)
    # messages where coach is a recepeint
    messages = db.query(m.Message).filter_by(receiver_id=coach.uuid).all()
    for message in messages:
        student = db.query(m.Student).filter_by(uuid=message.author_id).first()
        contacts.append(student)
    contacts: list = list(set(contacts))
    return s.UserList(users=contacts)


# get messages for current dialogue
@message_router.get(
    "/coach/messages/{student_uuid}",
    response_model=s.MessageList,
)
def get_coach_student_messages(
    student_uuid: str,
    student: m.Student = Depends(get_student_by_uuid),
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    messages: list[m.Message] = (
        db.query(m.Message)
        .filter_by(author_id=coach.uuid, receiver_id=student.uuid)
        .order_by(m.Message.created_at.desc())
        .all()
    )
    log(log.INFO, "found [%d] messages", len(messages))
    return s.MessageList(messages=messages)


@message_router.delete("/coach/messages/{student_uuid}", status_code=status.HTTP_200_OK)
def delete_coach_student_messages(
    student_uuid: str,
    student: m.Student = Depends(get_student_by_uuid),
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    messages = (
        db.query(m.Message)
        .filter_by(author_id=coach.uuid, receiver_id=student.uuid)
        .all()
    )
    for message in messages:
        message.is_deleted = True
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while deleting messages - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occured while deleting messages",
        )
    log(log.INFO, "Messages deleted - [%d]", len(messages))
    return status.HTTP_200_OK


# Routes for students


@message_router.post("/student/create", response_model=s.Message)
def student_create_message(
    message_data: s.MessageData,
    db: Session = Depends(get_db),
    student: m.Coach = Depends(get_current_student),
):
    message: m.Message = m.Message(
        author_id=student.uuid,
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
@message_router.get("/student/list-of-contacts", response_model=s.UserList)
def get_student_list_of_contacts(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    # messages where coach is owner
    messages: list[m.Message] = (
        db.query(m.Message).filter_by(author_id=student.uuid).all()
    )
    contacts: list = []
    for message in messages:
        coach = db.query(m.Coach).filter_by(uuid=message.receiver_id).first()
        contacts.append(coach)
    # messages where coach is a recepeint
    messages = db.query(m.Message).filter_by(receiver_id=student.uuid).all()
    for message in messages:
        coach = db.query(m.Coach).filter_by(uuid=message.author_id).first()
        contacts.append(coach)
    contacts = list(set(contacts))
    return s.UserList(users=contacts)


# get messages for current dialogue
@message_router.get(
    "/student/messages/{coach_uuid}",
    response_model=s.MessageList,
)
def get_student_coach_messages(
    coach_uuid: str,
    coach: m.Student = Depends(get_coach_by_uuid),
    db: Session = Depends(get_db),
    student: m.Coach = Depends(get_current_student),
):
    messages: list[m.Message] = (
        db.query(m.Message)
        .filter_by(author_id=student.uuid, receiver_id=coach.uuid)
        .order_by(m.Message.created_at.desc())
        .all()
    )
    log(log.INFO, "found [%d] messages", len(messages))
    return s.MessageList(messages=messages)


@message_router.delete("/student/messages/{coach_uuid}", status_code=status.HTTP_200_OK)
def delete_student_coach_messages(
    coach_uuid: str,
    coach: m.Student = Depends(get_coach_by_uuid),
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    messages = (
        db.query(m.Message)
        .filter_by(author_id=student.uuid, receiver_id=coach.uuid)
        .all()
    )
    for message in messages:
        message.is_deleted = True
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while deleting messages - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occured while deleting messages",
        )
    log(log.INFO, "Messages deleted - [%d]", len(messages))
    return status.HTTP_200_OK
