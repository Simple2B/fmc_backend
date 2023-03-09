from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str
    username: str
    is_verified: bool
    profile_picture: str | None

    class Config:
        orm_mode = True
