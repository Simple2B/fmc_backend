from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings, Settings
from app.logger import log
from app.database import get_db
import app.schema as s
import app.model as m

newsletter_router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@newsletter_router.post("/")
async def send_contact_request(
    data: s.NewsletterSubscription,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    subscription: m.NewsletterSubscription | None = (
        db.query(m.NewsletterSubscription).filter_by(email=data.email).first()
    )
    if subscription:
        log(log.INFO, "Newsletter Subscription for [%s] already exists", data.email)
        return Response(status_code=status.HTTP_208_ALREADY_REPORTED)

    subscription = m.NewsletterSubscription(
        email=data.email,
    )
    db.add(subscription)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(
            log.ERROR,
            "Failed to create a new newsletter subscription for: [%s] - [%s]",
            subscription.email,
            e,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed to create a new contact request",
        )
    log(log.INFO, "Newsletter Subscription for [%s] created", data.email)
    return Response(status_code=status.HTTP_201_CREATED)
