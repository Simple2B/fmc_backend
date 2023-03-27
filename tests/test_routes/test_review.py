from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


import app.model as m
import app.schema as s

from tests.fixture import TestData
from tests.utils import create_past_student_lesson


def test_review_notification(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens,
):
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    lesson = db.query(m.Lesson).first()
    assert lesson
    create_past_student_lesson(db=db, student_id=student.id, lesson_id=lesson.id)
    response = client.post(
        "api/notification/student/reviews",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.ReviewMessageList.parse_obj(response.json())
    assert resp_obj.messages[0].student.uuid == student.uuid
    assert resp_obj.messages[0].message_type == m.MessageType.REVIEW_COACH.value
