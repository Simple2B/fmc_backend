from typing import Generator

import pytest
from pydantic import BaseModel, EmailStr


class TestCoach(BaseModel):
    __test__ = False
    email: EmailStr
    password: str
    is_verified: bool | None


class TestStudent(BaseModel):
    __test__ = False
    email: EmailStr
    password: str
    is_verified: bool | None


class TestData(BaseModel):
    __test__ = False
    test_coaches: list[TestCoach] | None
    test_coach: TestCoach | None
    test_student: TestStudent | None


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    yield TestData.parse_file("tests/test_data.json")
