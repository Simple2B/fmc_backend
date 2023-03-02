# from shutil import unregister_archive_format
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schema import Token
from app.database import get_db
from app.model import Coach
from app.oauth2 import create_access_token


auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("coach/login", response_model=Token)
def login(
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
