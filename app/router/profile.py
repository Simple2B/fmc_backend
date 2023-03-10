from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError

from app.logger import log
from app.dependency import get_current_coach, get_current_student
from app.database import get_db
import app.schema as s
import app.model as m
from app.controller import create_s3_conn
from app.config import Settings, get_settings

profile_router = APIRouter(prefix="/profile", tags=["Profiles"])


@profile_router.get(
    "/coach",
    response_model=s.UserProfile,
)
def get_coach_profile(
    db: Session = Depends(get_db),
    coach=Depends(get_current_coach),
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
    student=Depends(get_current_student),
):
    return s.UserProfile(
        email=student.email,
        username=student.username,
        first_name=student.first_name,
        last_name=student.last_name,
        profile_picture=student.profile_picture,
        is_verified=student.is_verified,
    )


@profile_router.post("/coach/upload-image", status_code=status.HTTP_201_CREATED)
def upload_coach_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
    settings: Settings = Depends(get_settings),
):
    s3 = create_s3_conn(settings)
    try:
        file.file.seek(0)
        # Upload the file to to your S3 service
        s3.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET_NAME,
            f"user_profiles/pictures/{coach.uuid}/{file.filename}",
        )
    except ClientError as e:
        log(log.ERROR, "Error uploading file to S3 - [%s]", e)
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        file.file.close()
    # save to db
    coach.profile_picture = f"{settings.AWS_S3_BUCKET_URL}user_profiles/pictures/{coach.uuid}/{file.filename}"
    db.commit()
    return status.HTTP_200_OK
