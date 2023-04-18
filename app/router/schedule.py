from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from stripe.error import InvalidRequestError

from app.database import get_db, Session
from app.dependency import get_current_coach
from app.dependency.controller.stripe import get_stripe
from app.logger import log
import app.schema as s
import app.model as m

schedule_router = APIRouter(prefix="/schedule", tags=["Coach_Schedule"])


@schedule_router.get(
    "/schedules",
    status_code=status.HTTP_200_OK,
    response_model=s.ScheduleList,
)
def get_current_coach_schedules(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    schedules = (
        db.query(m.CoachSchedule).filter_by(coach_id=coach.id, is_deleted=False).all()
    )
    return s.ScheduleList(schedules=schedules)


@schedule_router.get(
    "/schedules/{coach_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=s.ScheduleList,
)
def get_coach_schedules_by_uuid(
    coach_uuid: str,
    location_id: int = None,
    schedule_date: str | None = datetime.now().date().isoformat(),
    db: Session = Depends(get_db),
):
    coach = db.query(m.Coach).filter_by(uuid=coach_uuid).first()
    if not coach:
        log(log.INFO, "Such coach not found - [%s]", coach_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Such coach not found",
        )
    query = db.query(m.CoachSchedule).filter(
        m.CoachSchedule.coach_id == coach.id,
        m.CoachSchedule.is_booked == False,  # noqa:flake8 E712
        m.CoachSchedule.is_deleted == False,  # noqa:flake8 E712
    )
    if location_id:
        query = query.join(m.Lesson).filter(m.Lesson.location_id == location_id)
    schedules = query.order_by(m.CoachSchedule.start_datetime.asc()).all()
    result = []
    for schedule in schedules:
        start_date = schedule.start_datetime.date()
        filter_date = datetime.strptime(schedule_date, "%Y-%m-%d").date()
        if start_date == filter_date:
            result.append(schedule)
    return s.ScheduleList(schedules=result)


@schedule_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_coach_schedule(
    data: s.BaseSchedule,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
    stripe=Depends(get_stripe),
):
    try:
        if not coach.stripe_account_id:
            log(log.INFO, "Coach [%s] does not have stripe account id", coach.email)
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="You didn`t connect to Stripe Connect",
            )
        account = stripe.Account.retrieve(coach.stripe_account_id)
        if not account["payouts_enabled"] and not account["charges_enabled"]:
            log(log.INFO, "Account is not ready for getting/sending payments")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not allowed to process payments.Please visit your stripe dashboard",
            )
        if (
            db.query(m.CoachSchedule)
            .filter_by(
                lesson_id=data.lesson_id,
                coach_id=coach.id,
                start_datetime=data.start_datetime,
                end_datetime=data.end_datetime,
            )
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Schedule already exists on this date",
            )
        if not data.lesson_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Missing package"
            )
        schedule = m.CoachSchedule(
            lesson_id=data.lesson_id,
            coach_id=coach.id,
            start_datetime=data.start_datetime,
            end_datetime=data.end_datetime,
        )

        db.add(schedule)
        db.commit()
    except InvalidRequestError as e:
        log(log.INFO, "Error while getting account data - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating schedule"
        )
    except SQLAlchemyError as e:
        log(log.INFO, "Error creating schedule for coach [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="Error creating schedule"
        )
    return status.HTTP_201_CREATED


@schedule_router.get(
    "/{schedule_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=s.Schedule,
)
def get_schedule_by_uuid(
    schedule_uuid: str,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    schedule = db.query(m.CoachSchedule).filter_by(uuid=schedule_uuid).first()
    if not schedule or schedule.is_deleted:
        log(log.INFO, "Schedule was not found or was deleted")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule was not found or was deleted",
        )
    return schedule


@schedule_router.delete(
    "/{schedule_uuid}",
    status_code=status.HTTP_200_OK,
)
def delete_schedule_by_uuid(
    schedule_uuid: str,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    schedule = db.query(m.CoachSchedule).filter_by(uuid=schedule_uuid).first()
    if not schedule:
        log(log.INFO, "Schedule was not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule was not found"
        )
    schedule.is_deleted = True
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while deleting schedule - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error while deleting schedule"
        )
    log(log.INFO, "Schedule deleted successfully - [%s]", schedule_uuid)
    return status.HTTP_200_OK


@schedule_router.put(
    "/{schedule_uuid}",
    status_code=status.HTTP_201_CREATED,
)
def edit_schedule(
    data: s.BaseSchedule,
    schedule_uuid: str,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    schedule = (
        db.query(m.CoachSchedule)
        .filter_by(uuid=schedule_uuid, is_deleted=False)
        .first()
    )
    if not schedule:
        log(log.INFO, "Schedule was not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule was not found"
        )
    schedule.lesson_id = data.lesson_id
    schedule.start_datetime = data.start_datetime
    schedule.end_datetime = data.end_datetime
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error while updating schedule - [%s]", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Schedule was not updated"
        )
    return status.HTTP_201_CREATED
