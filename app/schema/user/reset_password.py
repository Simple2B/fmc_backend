from pydantic import BaseModel


class UserResetPasswordIn(BaseModel):
    new_password: str
    new_password_confirmation: str
