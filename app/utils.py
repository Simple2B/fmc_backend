import uuid
from fastapi.routing import APIRoute


def generate_uuid() -> str:
    return str(uuid.uuid4())


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"
