# from shutil import unregister_archive_format
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log
from app.oauth2 import create_access_token
from app.database import get_db
import app.schema as s
from app.model import Coach, Student
from app.dependency import get_mail_client
from app.controller import MailClient


auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/coach/login", response_model=s.Token)
def coach_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    coach: Coach = Coach.authenticate(
        db,
        user_credentials.username,
        user_credentials.password,
    )

    if not coach:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": coach.id})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/student/login", response_model=s.Token)
def student_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    student: Student = Student.authenticate(
        db,
        user_credentials.username,
        user_credentials.password,
    )

    if not student:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": student.id})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/students/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(
    user_data: s.UserSignUp,
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
):
    student: Student | None = Student(**user_data.dict())
    db.add(student)
    try:
        log(log.INFO, "Creating a new student - [%s]", student.email)
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while singin up a new user - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while creating a student account",
        )
    return status.HTTP_200_OK
