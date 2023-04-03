from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_mail.errors import ConnectionErrors

from app.config import get_settings, Settings
from app.controller import MailClient
from app.dependency import get_mail_client
from app.logger import log
import app.schema as s


contact_router = APIRouter(prefix="/contact", tags=["Contact"])


@contact_router.post("/question", status_code=status.HTTP_200_OK)
async def send_contact_request(
    data: s.ContactDataIn,
    mail_client: MailClient = Depends(get_mail_client),
    settings: Settings = Depends(get_settings),
):
    try:
        await mail_client.send_email(
            settings.BUSINESS_EMAIL,
            "Contact question:",
            "contact_question.html",
            {
                "user_email": data.email_from,
                "message": data.message,
            },
        )
    except ConnectionErrors as e:
        log(log.ERROR, "Error while sending message - [%s]", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    log(log.INFO, "New contact request created from [%s]", data.email_from)
    return status.HTTP_200_OK
