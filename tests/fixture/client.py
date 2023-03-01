import pytest
from typing import Generator, Iterator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.schema as s
from .test_data import TestData


@pytest.fixture
def client() -> Generator:
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def authorized_client(
    client: TestClient,
    db: Session,
    test_data: TestData,
) -> Iterator[TestClient]:
    response = client.post(
        "api/login",
        data={
            "username": test_data.test_user.email,
            "password": test_data.test_user.password,
        },
    )

    assert response
    token = s.Token.parse_obj(response.json())
    client.headers["Authorization"] = f"Bearer {token.access_token}"
    yield client


@pytest.fixture
def authorized_client1(
    client: TestClient,
    db: Session,
    test_data: TestData,
) -> Generator[TestClient, None, None]:
    response = client.post(
        "api/login",
        data={
            "username": test_data.test_user1.email,
            "password": test_data.test_user1.password,
        },
    )

    assert response
    token = s.Token.parse_obj(response.json())
    client.headers["Authorization"] = f"Bearer {token.access_token}"
    yield client


@pytest.fixture
def authorized_tokens(
    client: TestClient,
    db: Session,
    test_data: TestData,
) -> Generator[list[s.Token], None, None]:
    tokens = []
    for user in test_data.test_users:
        response = client.post(
            "api/login",
            data={
                "username": user.email,
                "password": user.password,
            },
        )

        assert response
        token = s.Token.parse_obj(response.json())
        tokens += [token]
    yield tokens
