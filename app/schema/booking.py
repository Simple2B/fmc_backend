from pydantic import BaseModel


class Booking(BaseModel):
    lesson_uuid: str
