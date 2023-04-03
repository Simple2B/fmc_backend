from pydantic import BaseModel


class BaseUser(BaseModel):
    uuid: str | None = None
    email: str
