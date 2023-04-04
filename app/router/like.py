from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log

from app.dependency import get_current_student, get_coach_by_uuid
from app.database import get_db
import app.model as m
import app.schema as s

like_router = APIRouter(prefix="/like", tags=["Like"])


@like_router.post("/coach/{coach_uuid}", status_code=status.HTTP_201_CREATED)
def like_coach(
    coach_uuid: str,
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
    coach: m.Coach = Depends(get_coach_by_uuid),
):
    liked_coach = m.StudentFavouriteCoach(student_id=student.id, coach_id=coach.id)
    db.add(liked_coach)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while liking coach - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error while liking a coach"
        )
    return status.HTTP_201_CREATED


@like_router.post("/coach/unlike/{coach_uuid}", status_code=status.HTTP_201_CREATED)
def unlike_coach(
    coach_uuid: str,
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
    coach: m.Coach = Depends(get_coach_by_uuid),
):
    liked_coach = (
        db.query(m.StudentFavouriteCoach)
        .filter_by(student_id=student.id, coach_id=coach.id)
        .first()
    )
    db.delete(liked_coach)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while unliking coach - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error while unliking a coach"
        )
    return status.HTTP_201_CREATED


@like_router.get("/student/favourites", response_model=s.CoachList)
def list_liked_coached(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    return s.CoachList(coaches=student.favourites)
