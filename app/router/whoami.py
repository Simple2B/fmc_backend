from fastapi import APIRouter, status, Depends

from app.dependency import get_current_coach, get_current_student

whoami_router = APIRouter(prefix="/whoami", tags=["Whoami"])


@whoami_router.get("/student", status_code=status.HTTP_200_OK)
def whoami_student(current_student=Depends(get_current_student)):
    if current_student:
        return True


@whoami_router.get("/coach", status_code=status.HTTP_200_OK)
def whoami_coach(current_coach=Depends(get_current_coach)):
    if current_coach:
        return True
