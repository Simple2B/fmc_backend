from fastapi import APIRouter

from .coach_auth import coach_auth_router
from .student_auth import student_auth_router
from .user import router as user_router
from .whoami import whoami_router
from .profile import profile_router
from .keys import keys_router
from .contact import contact_router
from .sport import sport_router

router = APIRouter(prefix="/api")
router.include_router(student_auth_router)
router.include_router(coach_auth_router)
router.include_router(user_router)
router.include_router(whoami_router)
router.include_router(profile_router)
router.include_router(keys_router)
router.include_router(contact_router)
router.include_router(sport_router)
