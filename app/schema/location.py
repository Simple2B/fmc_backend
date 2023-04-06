from pydantic import BaseModel


class Location(BaseModel):
    uuid: str
    name: str | None
    city: str
    street: str
    postal_code: str

    class Config:
        orm_mode = True


class LocationList(BaseModel):
    locations: list[Location]
