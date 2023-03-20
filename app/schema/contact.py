from pydantic import BaseModel, EmailStr


class ContactDataIn(BaseModel):
    email_from: EmailStr  # Anonymous user
    message: str

    # TODO make validation to message length
