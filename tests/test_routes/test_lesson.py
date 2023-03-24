from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from tests.fixture import TestData
from tests.utils import create_student_lesson


def test_lesson(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens,
):
    # creatong appointment
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    lesson = db.query(m.Lesson).first()
    assert lesson
    create_student_lesson(db=db, student_id=student.id, lesson_id=lesson.id)

    response = client.get(
        "api/lesson/lessons/upcoming",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.UpcomingLessonList.parse_obj(response.json())
    assert resp_obj
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    upc_lessons = db.query(m.StudentLesson).filter_by(student_id=student.id).all()
    assert len(upc_lessons) == len(resp_obj.lessons)
