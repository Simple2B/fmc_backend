from pydantic import BaseModel, EmailStr


class NewsletterSubscription(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
