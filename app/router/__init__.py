from fastapi import APIRouter

from .coach_auth import coach_auth_router
from .student_auth import student_auth_router
from .user import router as user_router

router = APIRouter(prefix="/api")
router.include_router(student_auth_router)
router.include_router(coach_auth_router)
router.include_router(user_router)
