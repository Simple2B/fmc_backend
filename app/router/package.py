from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log

from app.dependency import get_current_coach
from app.database import get_db
import app.schema as s
import app.model as m

package_router = APIRouter(prefix="/package", tags=["Packages"])


@package_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_package(
    data: s.BaseLesson,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    if db.query(m.Lesson).filter_by(title=data.title).first():
        log(log.INFO, "Package with such title already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Package with such title already exists",
        )
    package = m.Lesson(
        title=data.title,
        coach_id=coach.id,
        location_id=data.location.id,
        sport_type_id=data.sport.id,
        about=data.about,
        max_people=data.max_people,
        price=data.price,
    )
    db.add(package)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while creating package - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occured while creating package",
        )
    log(log.INFO, "Package [%s] created successfully", package.uuid)
    return status.HTTP_201_CREATED


@package_router.get(
    "/packages", status_code=status.HTTP_201_CREATED, response_model=s.LessonList
)
def get_packages(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    return s.LessonList(lessons=coach.lessons)


@package_router.get(
    "/{package_uuid}", status_code=status.HTTP_201_CREATED, response_model=s.Lesson
)
def get_package(
    package_uuid: str,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    package = db.query(m.Lesson).filter_by(uuid=package_uuid).first()
    if not package:
        log(log.INFO, "Package [%s] not found", package_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package was not found"
        )

    return package
