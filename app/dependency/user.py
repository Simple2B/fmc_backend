from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app.schema import TokenData
from app.database import get_db
from app.model import Coach, Student
from app.config import Settings, get_settings

settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

http_exceptions: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_coach(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Coach:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
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
    if not coach.is_verified:
        return http_exceptions
    return coach


def get_current_student(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Student:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    id: str = payload.get("user_id")
    if not id:
        raise http_exceptions
    token_data = TokenData(id=id)
    student: Student | None = db.query(Student).filter_by(id=token_data.id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not student.is_verified:
        raise http_exceptions
    return student


def get_student_by_uuid(
    student_uuid: str,
    coach: Coach = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    student: Student = db.query(Student).filter_by(uuid=student_uuid).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Such student does not exist",
        )
    return student


def get_coach_by_uuid(
    coach_uuid: str,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    coach: Coach = db.query(Coach).filter_by(uuid=coach_uuid).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Such coach does not exist",
        )
    return coach
