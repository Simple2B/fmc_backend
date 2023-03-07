from pydantic import BaseModel


class ContactFormSchema(BaseModel):
    email_from: str
    message: str
