from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db, Session
from app.dependency import get_current_coach
from app.logger import log
import app.schema as s
import app.model as m

schedule_router = APIRouter(prefix="/schedule", tags=["Coach Schedule"])


@schedule_router.get(
    "/schedules",
    status_code=status.HTTP_200_OK,
    response_model=s.ScheduleList,
)
def get_current_coach_schedules(
    db: Session = Depends(get_db),
    coach: m.Coach = Depends(get_current_coach),
):
    return s.ScheduleList(schedules=coach.schedules)


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
            coach_id=data.coach_id,
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
        coach_id=data.coach_id,
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
