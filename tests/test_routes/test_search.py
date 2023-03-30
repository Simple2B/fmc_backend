from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.controller import MailClient
import app.model as m
import app.schema as s
from tests.fixture import TestData


def test_search_for_coach(
    client: TestClient,
    db: Session,
    test_data: TestData,
    mail_client: MailClient,
):
    name = test_data.test_coaches[0].first_name[0:3]
    response = client.get(f"api/search/coaches?first_name={name}")
    assert response.status_code == 200
    resp_obj = s.CoachList.parse_obj(response.json())
    assert resp_obj
    founded_coaches = (
        db.query(m.Coach)
        .filter(
            or_(m.Coach.first_name.icontains(name)),
            (m.Coach.last_name.icontains(name)),
        )
        .all()
    )
    # assert founded_coaches
    # assert len(resp_obj.coaches) == len(founded_coaches)
