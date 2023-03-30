from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from tests.fixture import TestData


def test_likes(
    client: TestClient,
    test_data: TestData,
    db: Session,
    authorized_student_tokens,
):
    coach = db.query(m.Coach).first()
    assert coach
    response = client.post(
        f"api/like/coach/{coach.uuid}",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response.status_code == 201
    assert db.query(m.StudentFavouriteCoach).count() > 0

    response = client.get(
        "api/like/coach/coaches",
        headers={
            "Authorization": f"Bearer {authorized_student_tokens[0].access_token}"
        },
    )
    assert response.status_code == 200
    resp_obj = s.CoachList.parse_obj(response.json())
    assert resp_obj
    coach = db.query(m.Coach).first()
    assert coach
    assert resp_obj.coaches[0].email == coach.email
