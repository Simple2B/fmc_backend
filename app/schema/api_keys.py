from pydantic import BaseModel


class GAPIKeysSchema(BaseModel):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
