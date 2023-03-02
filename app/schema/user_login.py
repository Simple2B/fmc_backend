from pydantic import BaseModel


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserGoogleLogin(BaseModel):
    """Scheme for validating user`s sign in via Google OAuth data"""

    email: str
    username: str
    google_openid_key: str
