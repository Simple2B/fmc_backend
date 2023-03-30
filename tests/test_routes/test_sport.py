from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.controller import MailClient
import app.model as m
import app.schema as s
from tests.fixture import TestData


def test_get_all_sports(
    client: TestClient,
    db: Session,
    test_data: TestData,
    mail_client: MailClient,
):
    sports = db.query(m.SportType).all()
    assert sports

    response = client.get("/api/sports/types")
    assert response
    resp_obj = s.ListSportType.parse_obj(response.json())
    assert resp_obj
    assert len(resp_obj.sport_types) == len(sports)
