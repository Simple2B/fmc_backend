from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.model as m
from app.database import get_db
import app.schema as s


sport_router = APIRouter(prefix="/sports", tags=["Sports"])


@sport_router.get(
    "/types",
    response_model=s.ListSportTypeSchema,
)
def get_sports(db: Session = Depends(get_db)):
    sport_types: list[m.SportType] = db.query(m.SportType).all()
    return s.ListSportTypeSchema(sport_types=sport_types)
