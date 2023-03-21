from typing import Generator

import pytest
from pydantic import BaseModel


class TestCoach(BaseModel):
    __test__ = False
    uuid: str | None
    email: str
    password: str
    username: str
    first_name: str | None
    last_name: str | None
    is_verified: bool | None
    profile_picture: str | None
    google_open_id: str | None


class TestStudent(BaseModel):
    __test__ = False
    uuid: str | None
    email: str
    username: str
    password: str
    is_verified: bool | None
    first_name: str | None
    last_name: str | None
    profile_picture: str | None
    google_open_id: str | None


class TestLocation(BaseModel):
    __test__ = False
    name: str
    street: str
    city: str
    state: str
    postal_code: str


class TestData(BaseModel):
    __test__ = False
    test_coaches: list[TestCoach]
    test_students: list[TestStudent]
    test_coach: TestCoach | None
    test_student: TestStudent | None
    # authorized
    test_authorized_students: list[TestStudent]
    test_authorized_coaches: list[TestCoach]

    test_locations: list[TestLocation]


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    yield TestData.parse_file("tests/test_data.json")
