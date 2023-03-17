from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_mail.errors import ConnectionErrors

from app.config import get_settings, Settings
from app.utils import generate_uuid
from app.controller import MailClient
from app.logger import log
from app.oauth2 import create_access_token
from app.database import get_db
from app.dependency import get_mail_client
import app.schema as s
from app.model import Student


student_auth_router = APIRouter(prefix="/auth/student", tags=["Student Authentication"])


@student_auth_router.post("/login", response_model=s.Token)
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


@student_auth_router.post("/sign-up", status_code=status.HTTP_200_OK)
async def student_sign_up(
    student_data: s.UserSignUp,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
):
    student: Student | None = Student(**student_data.dict(), is_verified=False)
    db.add(student)
    try:
        log(log.INFO, "New student is created: [%s]", student.email)
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to create a new student: [%s]\n[%s]", student.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with such email address already exists",
        )
    try:
        await mail_client.send_email(
            student.email,
            "Account activation",
            "email_verification.html",
            {
                "user_email": student.email,
                "verification_url": f"{settings.BASE_URL}{settings.CONFIRMATION_URL_STUDENT}?token={student.verification_token}",  # noqa E501
            },
        )
    except ConnectionErrors as e:
        db.rollback()
        log(log.ERROR, "Error while sending message - [%s]", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return status.HTTP_200_OK


@student_auth_router.get(
    "/account-confirmation/{token}", status_code=status.HTTP_200_OK
)
def student_account_confirmation(
    token: str,
    db: Session = Depends(get_db),
):
    student: Student | None = (
        db.query(Student).filter_by(verification_token=token).first()
    )
    if not student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad token")
    student.is_verified = True
    student.verification_token = generate_uuid()
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while approving an account",
        )
    log(log.INFO, "Student has been verified - [%s]", student.email)
    return status.HTTP_200_OK


@student_auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password_student(
    data: s.BaseUser,
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
    settings: Settings = Depends(get_settings),
):
    student: Student | None = db.query(Student).filter_by(email=data.email).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven`t been signed up before",
        )
    if not student.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven`t been verified before",
        )
    try:
        await mail_client.send_email(
            student.email,
            "Reseting password",
            "forgot_password_mail.html",
            {
                "user_email": student.email,
                "verification_link": f"{settings.BASE_URL}{settings.RESET_PASSWORD_URL_STUDENT}?token={student.verification_token}",  # noqa E501
            },
        )
    except ConnectionErrors as e:
        db.rollback()
        log(log.ERROR, "Error while sending message - [%s]", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    student.password = "*"
    db.commit()
    return status.HTTP_200_OK


@student_auth_router.post(
    "/reset-password/{verification_token}", status_code=status.HTTP_200_OK
)
def student_reset_password(
    verification_token: str,
    data: s.UserResetPasswordIn,
    db: Session = Depends(get_db),
):
    if data.new_password != data.new_password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords are not the same",
        )
    student: Student | None = (
        db.query(Student).filter_by(verification_token=verification_token).first()
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad token",
        )
    student.verification_token = generate_uuid()
    student.password = data.new_password
    db.commit()
    return status.HTTP_200_OK


@student_auth_router.post("/google-oauth", status_code=status.HTTP_200_OK)
def student_google_auth(
    student_data: s.UserGoogleLogin,
    db: Session = Depends(get_db),
):
    student: Student | None = (
        db.query(Student).filter_by(email=student_data.email).first()
    )
    if not student:
        student = Student(
            email=student_data.email,
            username=student_data.email,
            password="*",
            google_open_id=student_data.google_openid_key,
            is_verified=True,
            verification_token=generate_uuid(),
        )
        db.add(student)
        try:
            db.commit()
        except SQLAlchemyError as e:
            log(log.INFO, "Error - [%s]", e)
            raise HTTPException(
                status=status.HTTP_409_CONFLICT,
                detail="Error while saving creating a student",
            )
        log(
            log.INFO,
            "Student [%s] has been created (via Google account))",
            student.email,
        )
    if student_data.picture:
        student.picture = student_data.picture
        db.commit()
    student.authenticate(db, student.username, student.password)
    log(log.INFO, "Authenticating user - [%s]", student.email)
    access_token = create_access_token(data={"user_id": student.id})
    return s.Token(
        access_token=access_token,
        token_type="bearer",
    )
