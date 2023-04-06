from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from tests.fixture import TestData
from tests.utils import create_upcoming_student_lesson


def test_lesson(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens,
    authorized_coach_tokens,
):
    # creatong appointment
    student = (
        db.query(m.Student)
        .filter_by(email=test_data.test_authorized_students[0].email)
        .first()
    )
    assert student
    coach = (
        db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
    )
    assert coach
    schedule = db.query(m.CoachSchedule).filter_by(coach_id=coach.id).first()
    assert schedule
    create_upcoming_student_lesson(
        db=db,
        student_id=student.id,
        schedule_id=schedule.id,
        coach_id=coach.id,
    )

    response = client.get(
        "api/lesson/lessons/student/upcoming",
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

    # getting upcoming appointments for coach
    response = client.get(
        "api/lesson/lessons/coach/upcoming",
        headers={"Authorization": f"Bearer {authorized_coach_tokens[0].access_token}"},
    )
    assert response
    resp_obj = s.UpcomingLessonList.parse_obj(response.json())
    assert (
        resp_obj.lessons[0].schedule.coach.email
        == db.query(m.Coach)
        .filter_by(email=test_data.test_authorized_coaches[0].email)
        .first()
        .email
    )
