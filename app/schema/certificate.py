from datetime import datetime
from pydantic import BaseModel


class Certificate(BaseModel):
    certificate_url: str
    created_at: datetime

    class Config:
        orm_mode = True
