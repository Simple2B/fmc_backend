from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    email: EmailStr
    password: str
