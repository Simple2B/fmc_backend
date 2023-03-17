from pydantic import BaseModel


class BaseUser(BaseModel):
    uuid: str
    email: str
