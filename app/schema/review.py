from datetime import datetime

from pydantic import BaseModel


class BaseReview(BaseModel):
    text: str
    rate: int

    class Config:
        orm_mode = True


class Review(BaseReview):
    id: int
    uuid: str
    created_at: datetime

    class Config:
        orm_mode = True


class ReviewList(BaseModel):
    reviews: list[Review]
