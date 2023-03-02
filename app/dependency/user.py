from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from app.schema import TokenData
from app.database import get_db
from app.model import Coach
from app.config import Settings, get_settings

settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_coach(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Coach:
    payload = jwt.decode(token, settings.SECRET_KEY)
    id: str = payload.get("user_id")
    if not id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = TokenData(id=id)
    coach: Coach | None = db.query(Coach).filter_by(id=token_data.id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return coach
