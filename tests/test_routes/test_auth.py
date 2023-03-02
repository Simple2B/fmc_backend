from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controller import MailClient
from app.config import Settings
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_login(client: TestClient, db: Session, test_data: TestData):
    ...


def test_mail(mail_client: MailClient):
    with mail_client.mail.record_messages():
        ...
