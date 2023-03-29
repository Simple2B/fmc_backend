from datetime import datetime
from pydantic import BaseModel


class Certificate(BaseModel):
    certificate_url: str
    is_deleted: bool
    created_at: datetime

    class Config:
        orm_mode = True


class CertificateList(BaseModel):
    certificates: list[Certificate]
