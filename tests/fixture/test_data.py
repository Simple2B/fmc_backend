from typing import Generator

import pytest
from pydantic import BaseModel, EmailStr


class TestUser(BaseModel):
    __test__ = False
    username: str
    email: EmailStr
    password: str


class TestData(BaseModel):
    __test__ = False
    test_users: list[TestUser]
    test_user: TestUser
    test_user1: TestUser


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    yield TestData.parse_file("tests/test_data.json")
