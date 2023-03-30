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


@search_router.get("/", status_code=status.HTTP_200_OK)
def search_coaches(
    first_name: str | None,
    db: Session = Depends(get_db),
):
    query = db.query(m.Coach)
    if first_name:
        query.filter(
            or_(m.Coach.first_name.icontains(first_name)),
            (m.Coach.last_name.icontains(first_name)),
        )
    return query.all()
