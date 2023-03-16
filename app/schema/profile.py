from pydantic import BaseModel


class StudentProfileSchema(BaseModel):
    first_name: str
    last_name: str


class CoachProfileSchema(BaseModel):
    ...


class ProfileChangePassword(BaseModel):
    old_password: str
    new_password: str
    new_password_confirmation: str
