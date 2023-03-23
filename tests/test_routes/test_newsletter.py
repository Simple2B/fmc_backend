from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import status

from app import schema as s
from app import model as m


def test_create_subscription(client: TestClient, db: Session):
    TEST_EMAIL = "test@test8975290.com"
    assert db.query(m.NewsletterSubscription).count() == 0
    data = s.NewsletterSubscription(email=TEST_EMAIL).dict()
    res = client.post(
        "api/newsletter",
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
        "api/newsletter",
        json=data,
    )
    assert res
    assert db.query(m.NewsletterSubscription).count() == 1
    assert res.status_code == status.HTTP_208_ALREADY_REPORTED
