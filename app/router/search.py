from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_mail.errors import ConnectionErrors

from app.logger import log
from app.database import get_db
import app.schema as s
import app.model as m

search_router = APIRouter(prefix="/search", tags=["Search"])


@search_router.get(
    "/coaches", status_code=status.HTTP_200_OK, response_model=s.CoachList
)
def search_coaches(
    name: str = "",
    db: Session = Depends(get_db),
):
    query = db.query(m.Coach)
    query.filter(
        or_(
            m.Coach.last_name.ilike(f"%{name}%"),
            m.Coach.first_name.ilike(f"%{name}%"),
        )
    )
    return s.CoachList(coaches=query.all())
