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

    return s.Token(access_token=access_token, token_type="bearer")


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

    return s.Token(access_token=access_token, token_type="bearer")


@auth_router.post("/students/sign-up", status_code=status.HTTP_200_OK)
async def students_sign_up(
    student_data: s.UserSignUp,
    db: Session = Depends(get_db),
):
    student: Student | None = Student(**student_data.dict())
    db.add(student)
    try:
        log(log.INFO, "Creating a new student - [%s]", student.email)
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while singin up a new student - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while creating a student account",
        )
    return status.HTTP_200_OK


@auth_router.post("/coaches/sign-up", status_code=status.HTTP_200_OK)
async def coaches_sign_up(
    coach_data: s.UserSignUp,
    db: Session = Depends(get_db),
):
    coach: Coach | None = Coach(**coach_data.dict())
    db.add(coach)
    try:
        log(log.INFO, "Creating a new coach - [%s]", coach.email)
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while singin up a new coach - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while creating a coach account",
        )
    return status.HTTP_200_OK
