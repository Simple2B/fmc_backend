from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserGoogleLogin(BaseModel):
    """Scheme for validating user`s sign in via Google OAuth data"""

    email: str
    username: str
    google_openid_key: str
    picture: str | None


class UserResetPassword(BaseModel):
    password: str
    password1: str


class UserEmail(BaseModel):
    email: EmailStr
