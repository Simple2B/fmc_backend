from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from app.dependency.user import get_current_student

from app.logger import log
from app.database import get_db
import app.schema as s
import app.model as m

review_router = APIRouter(prefix="/review", tags=["Reviews"])


@review_router.post("/{session_uuid}")
def create_review(
    session_uuid: str,
    data: s.Review,
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    student_lesson = db.query(m.StudentLesson).filter_by(uuid=session_uuid).first()
    if not student_lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student lesson not found"
        )
    review = m.LessonReview(
        student_lesson_id=student_lesson.uuid,
        text=data.text,
        rate=data.rate,
    )
    db.add(review)
    # TODO logic for rewards - 1. Get price of session calcuate reward 2.Get rate and calculate reward
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Errow while creating a review - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occured while creating review",
        )
    return status.HTTP_200_OK
