from pydantic import BaseModel


class APIKeysSchema(BaseModel):
    google_client_id: str
