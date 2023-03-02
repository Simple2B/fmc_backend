from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log
from app.oauth2 import create_access_token
from app.database import get_db
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


@coach_auth_router.post("/google-oauth", status_code=status.HTTP_200_OK)
async def coach_google_auth(
    coach_data: s.UserGoogleLogin,
    db: Session = Depends(get_db),
):
    ...
