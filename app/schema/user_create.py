from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    email: EmailStr
    username: str
    password: str
