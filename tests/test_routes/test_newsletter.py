from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import status

from app import schema as s
from app import model as m
from app.controller import MailClient, send_daily_report


def test_create_subscription(client: TestClient, db: Session):
    TEST_EMAIL = "test@test8975290.com"
    assert db.query(m.NewsletterSubscription).count() == 0
    data = s.NewsletterSubscription(email=TEST_EMAIL).dict()
    res = client.post(
        "api/newsletter/subscribe",
        json=data,
    )
    assert res
    assert res.status_code == status.HTTP_201_CREATED

    assert db.query(m.NewsletterSubscription).count() == 1
    subscription: m.NewsletterSubscription = db.query(m.NewsletterSubscription).first()
    assert subscription
    assert subscription.email == TEST_EMAIL
    assert subscription.state == m.NewsletterSubscription.State.NEW

    res = client.post(
        "api/newsletter/subscribe",
        json=data,
    )
    assert res
    assert db.query(m.NewsletterSubscription).count() == 1
    assert res.status_code == status.HTTP_208_ALREADY_REPORTED


def test_daily_report(db: Session, mail_client: MailClient):
    from tasks.create_dummy_data import (
        create_dummy_newsletter_subscriptions,
        TEST_NEWSLETTER_NUMBER_TODAYS_NEW,
        TEST_NEWSLETTER_NUMBER_YESTERDAY_ACTIVE,
    )

    create_dummy_newsletter_subscriptions(db)
    assert (
        db.query(m.NewsletterSubscription).count()
        == TEST_NEWSLETTER_NUMBER_TODAYS_NEW + TEST_NEWSLETTER_NUMBER_YESTERDAY_ACTIVE
    )

    with mail_client.mail.record_messages() as outbox:
        send_daily_report()
        assert len(outbox) == 1
        letter = outbox[0]
        assert "@" in letter["To"]
