import uuid
import datetime


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_datetime() -> int:
    return int(datetime.datetime.now().timestamp())
