from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.config import Settings
import app.schema as s
import app.model as m
from tests.conftest import get_test_settings
from tests.fixture import TestData


settings: Settings = get_test_settings()


def test_message_coach(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens,
):
    # Testing message from coach to student
    student = db.query(m.Student).first()
    assert student
    request_data = s.MessageData(text="text message", receiver_id=student.uuid).dict()
    response = client.post(
        "api/message/coach/create",
        json=request_data,
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
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
    assert resp_obj.author.email == coach.email
    assert resp_obj.receiver.uuid == db.query(m.Student).first().uuid

    # Testing getting list of coach`s contacts`
    response = client.get(
        "api/message/coach/list-of-contacts",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.ContactList.parse_obj(response.json())
    student = db.query(m.Student).first()
    assert student
    assert resp_obj.contacts[0].user.uuid == student.uuid

    # Getting messages between coach and student
    response = client.get(
        f"api/message/coach/messages/{student.uuid}",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.MessageList.parse_obj(response.json())
    assert len(resp_obj.messages) == 1
    assert resp_obj.messages[0].author.uuid == coach.uuid
    assert resp_obj.messages[0].receiver.uuid == db.query(m.Student).first().uuid


def test_message_student(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens,
):
    # Testing email from coach to student
    coach = db.query(m.Coach).first()
    assert coach
    request_data = s.MessageData(text="text message", receiver_id=coach.uuid).dict()
    response = client.post(
        "api/message/student/create",
        json=request_data,
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.Message.parse_obj(response.json())
    assert resp_obj
    student: m.Student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    assert resp_obj.author.email == student.email
    assert resp_obj.receiver.uuid == db.query(m.Coach).first().uuid

    # Testing getting list of coach`s contacts`
    response = client.get(
        "api/message/student/list-of-contacts",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.ContactList.parse_obj(response.json())
    coach = db.query(m.Coach).first()
    assert coach
    assert resp_obj.contacts[0].user.uuid == coach.uuid

    # Getting messages between student and coach
    response = client.get(
        f"api/message/student/messages/{coach.uuid}",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.MessageList.parse_obj(response.json())
    assert len(resp_obj.messages) == 1
    assert resp_obj.messages[0].author.uuid == student.uuid
    assert resp_obj.messages[0].receiver.uuid == db.query(m.Coach).first().uuid
