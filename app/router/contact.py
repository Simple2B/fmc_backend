from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_mail.errors import ConnectionErrors

from app.config import get_settings, Settings
from app.controller import MailClient
from app.dependency import get_mail_client
from app.logger import log
from app.database import get_db
import app.schema as s
import app.model as m

contact_router = APIRouter(prefix="/contact", tags=["Contact"])


@contact_router.post("/question", status_code=status.HTTP_200_OK)
async def send_contact_request(
    data: s.ContactDataIn,
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
    settings: Settings = Depends(get_settings),
):
    contact: m.Contact = m.Contact(
        email_from=data.email_from,
        message=data.message,
    )
    db.add(contact)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(
            log.ERROR,
            "Failed to create a new contact request from: [%s]\n[%s]",
            contact.email_from,
            e,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed to create a new contact request",
        )
    try:
        await mail_client.send_email(
            settings.BUSINESS_EMAIL,
            "Contact question:",
            "contact_question.html",
            {
                "user_email": contact.email_from,
                "message": contact.message,
            },
        )
    except ConnectionErrors as e:
        log(log.ERROR, "Error while sending message - [%s]", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    log(log.INFO, "New contact request created from [%s]", contact.email_from)
    return status.HTTP_200_OK
