from pydantic import BaseModel


class SportTypeSchema(BaseModel):
    uuid: str
    name: str

    class Config:
        orm_mode = True


class ListSportTypeSchema(BaseModel):
    sport_types: list[SportTypeSchema]

    class Config:
        orm_mode = True
