from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_mail.errors import ConnectionErrors

from app.utils import generate_uuid
from app.logger import log
from app.controller import MailClient
from app.oauth2 import create_access_token
from app.database import get_db
from app.dependency import get_mail_client
import app.schema as s
from app.model import Coach


coach_auth_router = APIRouter(prefix="/auth/coach", tags=["Coach Authentication"])


@coach_auth_router.post("/login", response_model=s.Token)
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


@coach_auth_router.post("/sign-up", status_code=status.HTTP_200_OK)
async def coach_sign_up(
    coach_data: s.UserSignUp,
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
):
    coach: Coach | None = Coach(**coach_data.dict(), is_verified=False)
    db.add(coach)
    try:
        await mail_client.send_email(
            coach.email,
            "Account activation",
            "email_verification.html",
            {
                "user_email": coach.email,
                "verification_token": coach.verification_token,
            },
        )
    except ConnectionErrors as e:
        db.rollback()
        log(log.ERROR, "Error while sending message - [%s]", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

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


@coach_auth_router.get("/account-confirmation", status_code=status.HTTP_200_OK)
def coach_account_confirmation(
    token: str,
    db: Session = Depends(get_db),
):
    coach: Coach | None = db.query(Coach).filter_by(verification_token=token).first()
    if not coach:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad token")
    coach.is_verified = True
    coach.verification_token = generate_uuid()
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while approving an account",
        )


@coach_auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    data: s.UserEmail,
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
):
    coach: Coach | None = db.query(Coach).filter_by(email=data.email).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven`t been signed up before",
        )
    if not coach.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coach hasn`t been verified before",
        )
    try:
        await mail_client.send_email(
            coach.email,
            "Reseting password",
            "forgot_password_mail.html",
            {
                "user_email": coach.email,
                "verification_token": coach.verification_token,
            },
        )
    except ConnectionErrors as e:
        db.rollback()
        log(log.ERROR, "Error while sending message - [%s]", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    coach.password = "*"
    db.commit()
    return status.HTTP_200_OK


@coach_auth_router.post(
    "/reset-password/{verification_token}", status_code=status.HTTP_200_OK
)
def coach_reset_password(
    verification_token: str,
    data: s.UserResetPassword,
    db: Session = Depends(get_db),
):
    if data.password != data.password1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords are not the same",
        )
    coach: Coach | None = (
        db.query(Coach).filter_by(verification_token=verification_token).first()
    )
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad token",
        )
    coach.verification_token = generate_uuid()
    coach.password = data.password
    db.commit()
    return status.HTTP_200_OK


@coach_auth_router.post("/google-oauth", status_code=status.HTTP_200_OK)
async def coach_google_auth(
    coach_data: s.UserGoogleLogin,
    db: Session = Depends(get_db),
):
    return {}


# todo migrate back to invoke cli tool
