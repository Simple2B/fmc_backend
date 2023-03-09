from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_current_coach, get_current_student
from app.database import get_db
import app.schema as s


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
