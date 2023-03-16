from pydantic import BaseModel


class StudentProfileSchema(BaseModel):
    first_name: str
    last_name: str


class CoachProfileSchema(BaseModel):
    ...
