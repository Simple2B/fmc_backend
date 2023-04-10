from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, Session
from app.dependency import get_current_coach
from app.logger import log
import app.schema as s
import app.model as m

schedule_router = APIRouter(prefix="/schedule", tags=["Coach_Schedule"])


@schedule_router.get(
    "/schedules/{coach_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=s.ScheduleList,
)
def get_coach_schedules_by_uuid(
    coach_uuid: str,
    schedule_date: str | None = datetime.now().date(),
    db: Session = Depends(get_db),
):
    coach = db.query(m.Coach).filter_by(uuid=coach_uuid).first()
    if not coach:
        log(log.INFO, "Such coach not found - [%s]", coach_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Such coach not found",
        )
    schedules = (
        db.query(m.CoachSchedule)
        .filter(
            m.CoachSchedule.coach_id == coach.id,
            m.CoachSchedule.is_booked == False,  # noqa:flake8 E712
            m.CoachSchedule.start_datetime == schedule_date,
        )
        .order_by(m.CoachSchedule.start_datetime.asc())
    ).all()

    return s.ScheduleList(schedules=schedules)


@schedule_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_coach_schedule(
    data: s.BaseSchedule,
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    # check if such schedule already exists
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
    schedule = m.CoachSchedule(
        lesson_id=data.lesson_id,
        coach_id=coach.id,
        start_datetime=data.start_datetime,
        end_datetime=data.end_datetime,
    )

    db.add(schedule)
    try:
        db.commit()
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
    if not schedule:
        log(log.INFO, "Schedule was not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule was not found"
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
    db.delete(schedule)
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
    schedule = db.query(m.CoachSchedule).filter_by(uuid=schedule_uuid).first()
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
