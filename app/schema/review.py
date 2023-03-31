from pydantic import BaseModel


class Review(BaseModel):
    text: str
    rate: int

    class Config:
        orm_mode = True