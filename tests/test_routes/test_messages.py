from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.config import Settings
import app.schema as s
import app.model as m
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_create_message(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens,
):
    # Testing email from coach to student
    client.headers[
        "Authorization"
    ] = f"Bearer {authorized_coach_tokens[0].access_token}"

    student = db.query(m.Student).first()
    assert student
    request_data = s.MessageCreate(
        message_text="text message", message_to=student.uuid
    ).dict()
    response = client.post(
        "api/message/coach/send-message",
        json=request_data,
    )
    assert response
    resp_obj = s.Message.parse_obj(response.json())
    assert resp_obj
    coach: m.Coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    assert resp_obj.message_from == coach.uuid
    assert resp_obj.message_to == db.query(m.Student).first().uuid

    # Testing getting list of coach`s contacts`
    response = client.get(
        "api/message/coach/list-of-contacts",
    )
    assert response
    resp_obj = s.MessageUsersList.parse_obj(response.json())
    student = db.query(m.Student).first()
    assert student
    assert resp_obj.users[0].uuid == student.uuid

    # Getting messages between coach and student
    response = client.get(
        f"api/message/coach/messages/{student.uuid}",
    )
    assert response
    resp_obj = s.MessageList.parse_obj(response.json())
    assert len(resp_obj.messages) == 1
    assert resp_obj.messages[0].message_from == coach.uuid
    assert resp_obj.messages[0].message_to == db.query(m.Student).first().uuid
