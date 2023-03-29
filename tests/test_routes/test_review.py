from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


import app.model as m
import app.schema as s

from tests.fixture import TestData
from tests.utils import create_past_student_lesson


def test_leave_review(
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
    # TODO
    response = client.get(
        "api/notification/student/reviews",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response
    resp_obj = s.UnreviewedLessonsList.parse_obj(response.json())
    assert resp_obj
    lesson = db.query(m.Lesson).first()
    assert lesson
    # making sure its the right coach for this lesson
    assert resp_obj.lessons[0].coach.uuid == lesson.coach.uuid
    lesson_uuid = resp_obj.lessons[0].uuid
    assert db.query(m.StudentLesson).filter_by(uuid=lesson_uuid).first()

    # getting info about this lesson
    request_data = s.Review(text="This coach is super", rate=5).dict()
    response = client.post(
        f"api/review/{lesson_uuid}",
        json=request_data,
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response.status_code == 200
    assert db.query(m.LessonReview).all() is not None

    # making sure that review exists for this lesson
    assert db.query(m.StudentLesson).filter_by(uuid=lesson_uuid).first().review_id
