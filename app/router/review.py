from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from app.dependency import get_current_student, get_current_coach, get_lesson_by_uuid

from app.logger import log
from app.database import get_db
import app.schema as s
import app.model as m

review_router = APIRouter(prefix="/review", tags=["Reviews"])


@review_router.post("/{lesson_uuid}", status_code=status.HTTP_201_CREATED)
def create_review(
    data: s.BaseReview,
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
    lesson=Depends(get_lesson_by_uuid),
):
    review = m.LessonReview(
        student_lesson_id=lesson.id,
        text=data.text,
        rate=data.rate,
        coach_id=lesson.schedule.coach_id,
    )
    db.add(review)
    db.flush()
    lesson.review_id = review.id
    # TODO logic for rewards - 1. Get price of session calcuate reward 2.Get rate and calculate reward
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Errow while creating a review - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occured while creating review",
        )
    log(log.INFO, "Review has been created for lesson - [%s]", lesson.id)
    return status.HTTP_201_CREATED


@review_router.get(
    "/reviews", status_code=status.HTTP_200_OK, response_model=s.ReviewList
)
def coach_reviews_list(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    return s.ReviewList(reviews=coach.reviews)
