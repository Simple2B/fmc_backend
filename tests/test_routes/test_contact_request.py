from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controller import MailClient
from app.config import Settings
import app.schema as s
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_contact_form(
    client: TestClient,
    test_data: TestData,
    db: Session,
    mail_client: MailClient,
):
    with mail_client.mail.record_messages() as outbox:
        request_data = s.ContactDataIn(
            email_from="test@email.com", message="Hi i got a question ..."
        ).dict()
        response = client.post("api/contact/", json=request_data)
        assert response
        assert len(outbox) == 1
        resp_obj = s.BaseUser.parse_obj(response.json())
        assert resp_obj
        assert resp_obj.email == request_data.get("email_from")
