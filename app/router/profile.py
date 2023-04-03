import json

from fastapi import (
    APIRouter,
    Depends,
    Query,
    UploadFile,
    File,
    status,
    HTTPException,
    Form,
)
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log
from app.dependency import get_current_coach, get_current_student, get_s3_conn
from app.database import get_db
import app.schema as s
import app.model as m
from app.hash_utils import hash_verify
from app.config import Settings, get_settings


profile_router = APIRouter(prefix="/profile", tags=["Profiles"])


@profile_router.get(
    "/info/coach",
    response_model=s.Coach,
)
def get_info_coach_profile(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    return coach


@profile_router.get(
    "/coach",
    response_model=s.User,
)
def get_coach_profile(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    return s.User(
        uuid=coach.uuid,
        email=coach.email,
        username=coach.username,
        first_name=coach.first_name,
        last_name=coach.last_name,
        profile_picture=coach.profile_picture,
        is_verified=coach.is_verified,
    )


@profile_router.get("/coach/{coach_uuid}", response_model=s.Coach)
def get_coach_by_uuid(
    coach_uuid: str,
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    coach = db.query(m.Coach).filter_by(uuid=coach_uuid).first()
    return coach


@profile_router.get(
    "/student",
    response_model=s.User,
)
def get_student_profile(
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
):
    return s.User(
        uuid=student.uuid,
        email=student.email,
        username=student.username,
        first_name=student.first_name,
        last_name=student.last_name,
        profile_picture=student.profile_picture,
        is_verified=student.is_verified,
    )


@profile_router.get("/coach/subscription/info", response_model=s.Subscription)
def get_coach_subscription(
    db: Session = Depends(get_db),
    coach: m.Student = Depends(get_current_coach),
):
    subscription = db.query(m.CoachSubscription).filter_by(coach_id=coach.id).first()
    if not subscription:
        log(log.INFO, "Subscription not found for coach - [%s]", coach.email)
        return JSONResponse(status_code=status.HTTP_200_OK, content="Not found")
    return s.Subscription(
        product=subscription.product,
        stripe_subscription_id=subscription.stripe_subscription_id,
        current_period_end=subscription.current_period_end,
        current_period_start=subscription.current_period_start,
        created=subscription.created,
        status=subscription.status,
        is_active=subscription.is_active,
    )


@profile_router.post("/coach/personal-info", status_code=status.HTTP_201_CREATED)
async def update_coach_personal_info(
    file: UploadFile = File(None),
    first_name: str = Form(...),
    last_name: str = Form(""),
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
    settings: Settings = Depends(get_settings),
    s3=Depends(get_s3_conn),
):
    if file or not file.filename:
        try:
            file.file.seek(0)
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
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to update a profile for - [%s]\n[%s]", coach.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while updating profile",
        )
    log(log.INFO, "Saving profile for coach [%s]", coach.email)
    return status.HTTP_200_OK


@profile_router.post("/student/personal-info", status_code=status.HTTP_201_CREATED)
def update_student_personal_info(
    file: UploadFile = File(...),
    first_name: str = Form(...),
    last_name: str = Form(""),
    db: Session = Depends(get_db),
    student: m.Student = Depends(get_current_student),
    settings: Settings = Depends(get_settings),
    s3=Depends(get_s3_conn),
):
    if file:
        try:
            file.file.seek(0)
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
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to update a profile for - [%s]\n[%s]", student.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while uploading profile picture url",
        )
    log(log.INFO, "Updating profile for student [%s]", student.email)
    return status.HTTP_200_OK


@profile_router.post("/coach/profile-info", status_code=status.HTTP_201_CREATED)
def update_coach_profile(
    sport_category: str = Form(None),
    about: str | None = Form(None),
    certificates: list[UploadFile] = Form(None),
    deleted_certificates: str = Form(None),
    is_for_adult: bool | None = Form(None),
    is_for_children: bool | None = Form(None),
    locations: str | None = Form(None),
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
    settings: Settings = Depends(get_settings),
    s3=Depends(get_s3_conn),
):
    if about:
        coach.about = about
    coach.is_for_adults = is_for_adult
    coach.is_for_children = is_for_children
    if sport_category:
        parse_sport_category = json.loads(sport_category)
        for sport_type in parse_sport_category:
            sport = db.query(m.SportType).filter_by(name=sport_type).first()
            if not sport:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sport Category was not found",
                )
            coach_sports = db.query(m.CoachSport).filter_by(coach_id=coach.id).all()
            for coach_sport in coach_sports:
                db.delete(coach_sport)
                db.flush()
            db.add(m.CoachSport(coach_id=coach.id, sport_id=sport.id))
            log(log.INFO, "Coach sport created - [%s]", sport.name)
    if certificates:
        for certificate in certificates:
            try:
                certificate.file.seek(0)
                # Upload the file to to your S3 service
                s3.upload_fileobj(
                    certificate.file,
                    settings.AWS_S3_BUCKET_NAME,
                    f"user_profiles/certificates/coaches/{coach.uuid}/{certificate.filename}",
                )
            except ClientError as e:
                log(log.ERROR, "Error uploading certificate to S3 - [%s]", e)
                raise HTTPException(status_code=500, detail="Something went wrong")
            finally:
                certificate.file.close()
            # save to db
            coach.certificate_url = f"{settings.AWS_S3_BUCKET_URL}user_profiles/certificates/coaches/{coach.uuid}/{certificate.filename}"  # noqa:E501
            find_certificate = (
                db.query(m.Certificate)
                .filter_by(
                    certificate_url=coach.certificate_url,
                )
                .first()
            )
            if not find_certificate:
                db.add(
                    m.Certificate(
                        coach_id=coach.id, certificate_url=coach.certificate_url
                    )
                )
                db.flush()
    if deleted_certificates:
        parse_deleted_certificates = json.loads(deleted_certificates)
        log(log.INFO, "Deleted certificates - [%s]", parse_deleted_certificates)
        for deleted_certificate in parse_deleted_certificates:
            certificate = (
                db.query(m.Certificate)
                .filter_by(
                    coach_id=coach.id,
                    certificate_url=deleted_certificate,
                )
                .first()
            )
            if not certificate:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Certificate was not found",
                )
            certificate.is_deleted = True
            db.add(certificate)
            db.flush()
    if locations:
        db.query(m.CoachLocation).filter_by(coach_id=coach.id).delete()
        db.commit()
        parse_locations = json.loads(locations)
        for coach_location in parse_locations:
            location = (
                db.query(m.Location)
                .filter_by(
                    city=coach_location["city"],
                    street=coach_location["street"],
                    postal_code=coach_location["postal_code"],
                )
                .first()
            )
            if not location:
                location = m.Location(
                    city=coach_location["city"],
                    street=coach_location["street"],
                    postal_code=coach_location["postal_code"],
                )
                db.add(location)
                db.flush()
            db.add(m.CoachLocation(coach_id=coach.id, location_id=location.id))
            db.flush()

    db.commit()
    log(log.INFO, "Updating profile for coach - [%s]", coach.email)

    return status.HTTP_200_OK


@profile_router.post("/coach/change-password", status_code=status.HTTP_200_OK)
def coach_change_password(
    data: s.ProfileChangePasswordIn,
    coach: m.Coach = Depends(get_current_coach),
    db: Session = Depends(get_db),
):
    if not hash_verify(data.old_password, coach.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )
    if data.new_password != data.new_password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match",
        )
    coach.password = data.new_password
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to change password for - [%s]\n[%s]", coach.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while changing password",
        )
    log(log.INFO, "Changing password for coach - [%s]", coach.email)
    return status.HTTP_200_OK


@profile_router.post("/student/change-password", status_code=status.HTTP_200_OK)
def student_change_password(
    data: s.ProfileChangePasswordIn,
    student: m.Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    if not hash_verify(data.old_password, student.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )
    if data.new_password != data.new_password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match",
        )
    student.password = data.new_password
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Failed to change password for - [%s]\n[%s]", student.email, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error while changing password",
        )
    log(log.INFO, "Changing password for coach - [%s]", student.email)
    return status.HTTP_200_OK


@profile_router.get(
    "/profiles/search/cards", status_code=status.HTTP_200_OK, response_model=s.CoachList
)
def get_coach_cards(
    name: str | None = None,
    sport_ids: list[int] | None = Query(None),
    city: str | None = None,
    postal_code: str | None = None,
    db: Session = Depends(get_db),
):
    """Returns all cards for UNauthorized user"""
    # TODO search logic
    query = db.query(m.Coach)
    if name:
        query = query.filter(
            or_(
                m.Coach.last_name.icontains(f"{name}"),
                m.Coach.first_name.icontains(f"{name}"),
            )
        )
    if sport_ids:
        coach_sports = (
            db.query(m.CoachSport).filter(m.CoachSport.sport_id.in_(sport_ids)).all()
        )
        coach_ids = [cs.coach_id for cs in coach_sports]
        query = query.filter(m.Coach.id.in_(coach_ids))
    return s.CoachList(coaches=query.all())
