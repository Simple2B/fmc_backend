import asyncio

from fastapi_mail.errors import ConnectionErrors

from app.database import get_db, Session
from app import model as m
from app.logger import log
from .mail_client import MailClient
from app.config import get_settings


def send_daily_report():
    log(log.INFO, "Sending newsletter daily report")
    settings = get_settings()

    db: Session = get_db().__next__()
    new_subscriptions = (
        db.query(m.NewsletterSubscription)
        .filter_by(state=m.NewsletterSubscription.State.NEW)
        .all()
    )

    if not new_subscriptions:
        log(log.INFO, "No new Newsletter Subscriptions")
        return

    async def send_email():
        mail = MailClient(settings)

        try:
            await mail.send_email(
                settings.NEWSLETTER_REPORT_EMAIL,
                "New Newsletter Subscriptions",
                "daily_report.html",
                {"subscriptions": new_subscriptions, "len": len},
            )

            for sub in new_subscriptions:
                sub.state = m.NewsletterSubscription.State.ACTIVE
            db.commit()

        except ConnectionErrors as e:
            log(
                log.ERROR, "Cannot send daily Newsletter Subscriptions Report - [%s]", e
            )
        log(
            log.INFO,
            "Newsletter Subscriptions Report sent to [%s]",
            settings.NEWSLETTER_REPORT_EMAIL,
        )

    loop = asyncio.get_event_loop()
    coroutine = send_email()
    loop.run_until_complete(coroutine)
