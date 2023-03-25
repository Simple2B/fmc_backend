from pydantic import BaseModel


class SportType(BaseModel):
    uuid: str
    name: str

    class Config:
        orm_mode = True


class ListSportType(BaseModel):
    sport_types: list[SportType]
