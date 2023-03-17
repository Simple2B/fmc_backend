from pydantic import AnyHttpUrl
from .base import BaseUser


class UserGoogleLogin(BaseUser):
    """Scheme for validating user`s sign in via Google OAuth data"""

    username: str
    google_openid_key: str
    picture: AnyHttpUrl | None
