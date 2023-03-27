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
    authorized_student_tokens,
):
    # Testing message from coach to student
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
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
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    assert resp_obj.receiver.uuid == student.uuid

    # Testing getting list of coach`s contacts`
    response = client.get(
        "api/message/coach/list-of-contacts",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.ContactList.parse_obj(response.json())
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
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
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert resp_obj.messages[0].receiver.uuid == student.uuid
    assert resp_obj.messages[0].is_read == False  # noqa:flake8 E712

    # getting unread messages from coach
    response = client.get(
        "api/notification/student/new",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.MessageCount.parse_obj(response.json())
    assert db.query(m.Message).count() == resp_obj.count

    # setting message as read
    response = client.post(
        f"api/message/coach/messages/{student.uuid}/read",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    message = db.query(m.Message).first()
    assert message.is_read == False  # noqa:flake8 E712


def test_message_student(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_coach_tokens,
    authorized_student_tokens,
):
    # Testing email from coach to student
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
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
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    assert resp_obj.receiver.uuid == coach.uuid

    # Testing getting list of coach`s contacts`
    response = client.get(
        "api/message/student/list-of-contacts",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.ContactList.parse_obj(response.json())
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
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
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    assert resp_obj.messages[0].receiver.uuid == coach.uuid

    # getting unread messages from student
    response = client.get(
        "api/notification/coach/new",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.MessageCount.parse_obj(response.json())
    assert db.query(m.Message).count() == resp_obj.count

    # setting message as read
    response = client.post(
        f"api/message/student/messages/{coach.uuid}/read",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    message = db.query(m.Message).first()
    assert message.is_read == False  # noqa:flake8 E712
