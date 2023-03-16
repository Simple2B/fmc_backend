from pydantic import BaseModel


class UserSignUp(BaseModel):
    email: str
    username: str
    password: str
