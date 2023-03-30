from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.dependency.user import get_current_student
from app.logger import log
from app.database import get_db
import app.model as m


def get_lesson_by_uuid(
    lesson_uuid: str,
    student: m.Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    lesson: m.StudentLesson = (
        db.query(m.StudentLesson).filter_by(uuid=lesson_uuid).first()
    )
    if not lesson:
        log(log.INFO, "Lesson with this uuid does not exist - [%s]", lesson_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson does not exist",
        )
    return lesson
