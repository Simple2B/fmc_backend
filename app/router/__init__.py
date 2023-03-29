from fastapi import APIRouter, Request

from .coach_auth import coach_auth_router
from .student_auth import student_auth_router
from .whoami import whoami_router
from .profile import profile_router
from .keys import keys_router
from .contact import contact_router
from .sport import sport_router
from .message import message_router
from .lesson import lesson_router
from .newsletter import newsletter_router
from .stripe import stripe_router
from .subscription import subscription_router
from .notifications import notifications_router
from .review import review_router

router = APIRouter(prefix="/api")
router.include_router(student_auth_router)
router.include_router(coach_auth_router)
router.include_router(whoami_router)
router.include_router(profile_router)
router.include_router(keys_router)
router.include_router(contact_router)
router.include_router(sport_router)
router.include_router(message_router)
router.include_router(lesson_router)
router.include_router(newsletter_router)
router.include_router(stripe_router)
router.include_router(subscription_router)
router.include_router(notifications_router)
router.include_router(review_router)


@router.get("/list-endpoints/")
def list_endpoints(request: Request):
    url_list = [
        {"path": route.path, "name": route.name} for route in request.app.routes
    ]
    return url_list
