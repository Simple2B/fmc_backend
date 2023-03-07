from typing import Generator

import pytest
from pydantic import BaseModel, EmailStr


class TestCoach(BaseModel):
    __test__ = False
    email: EmailStr
    password: str
    username: str
    first_name: str | None
    last_name: str | None
    is_verified: bool | None


class TestStudent(BaseModel):
    __test__ = False
    email: EmailStr
    username: str
    password: str
    is_verified: bool | None
    first_name: str | None
    last_name: str | None


class TestData(BaseModel):
    __test__ = False
    test_coaches: list[TestCoach]
    test_students: list[TestStudent]
    test_coach: TestCoach | None
    test_student: TestStudent | None
    # authorized
    test_authorized_students: list[TestStudent]
    test_authorized_coaches: list[TestCoach]


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    yield TestData.parse_file("tests/test_data.json")
