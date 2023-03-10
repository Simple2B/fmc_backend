from pydantic import BaseModel


class APIKeysSchema(BaseModel):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
