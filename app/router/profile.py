from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    status,
    HTTPException,
    Form,
)
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log
from app.dependency import get_current_coach, get_current_student, get_s3_conn
from app.database import get_db
import app.schema as s
import app.model as m
from app.config import Settings, get_settings

profile_router = APIRouter(prefix="/profile", tags=["Profiles"])


@profile_router.get(
    "/coach",
    response_model=s.UserProfile,
)
def get_coach_profile(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    return s.UserProfile(
        email=coach.email,
        username=coach.username,
        first_name=coach.first_name,
        last_name=coach.last_name,
        profile_picture=coach.profile_picture,
        is_verified=coach.is_verified,
    )


@profile_router.get(
    "/student",
    response_model=s.UserProfile,
)
def get_student_profile(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    return s.UserProfile(
        email=student.email,
        username=student.username,
        first_name=student.first_name,
        last_name=student.last_name,
        profile_picture=student.profile_picture,
        is_verified=student.is_verified,
    )


@profile_router.post("/coach/personal-info", status_code=status.HTTP_201_CREATED)
async def update_coach_personal_info(
    file: UploadFile = File(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
    settings: Settings = Depends(get_settings),
    s3=Depends(get_s3_conn),
):
    try:
        file.file.seek(0)
        # Upload the file to to your S3 service
        s3.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET_NAME,
            f"user_profiles/pictures/coaches/pictures/{coach.uuid}/{file.filename}",
        )
    except ClientError as e:
        log(log.ERROR, "Error uploading file to S3 - [%s]", e)
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        file.file.close()
    # save to db
    coach.profile_picture = f"{settings.AWS_S3_BUCKET_URL}user_profiles/pictures/coaches/pictures/{coach.uuid}/{file.filename}"  # noqa:E501
    coach.first_name = first_name
    coach.last_name = last_name
    try:
        log(log.INFO, "Saving profile for coach [%s]", coach.email)
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to update a profile for - [%s]\n[%s]", coach.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while updating profile",
        )
    return status.HTTP_200_OK


@profile_router.post("/student/personal-info", status_code=status.HTTP_201_CREATED)
def update_student_personal_info(
    file: UploadFile = File(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
    settings: Settings = Depends(get_settings),
    s3=Depends(get_s3_conn),
):
    try:
        file.file.seek(0)
        # Upload the file to to your S3 service
        s3.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET_NAME,
            f"user_profiles/pictures/students/pictures/{student.uuid}/{file.filename}",
        )
    except ClientError as e:
        log(log.ERROR, "Error uploading file to S3 - [%s]", e)
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        file.file.close()
    # save to db
    student.profile_picture = f"{settings.AWS_S3_BUCKET_URL}user_profiles/pictures/students/pictures/{student.uuid}/{file.filename}"  # noqa:E501
    student.first_name = first_name
    student.last_name = last_name
    try:
        log(log.INFO, "Updating profile for student [%s]", student.email)
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to update a profile for - [%s]\n[%s]", student.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while uploading profile picture url",
        )
    return status.HTTP_200_OK
