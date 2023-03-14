from fastapi import APIRouter, Depends

import app.schema as s
from app.config import get_settings, Settings

keys_router = APIRouter(prefix="/keys", tags=["Keys"])


@keys_router.get("/", response_model=s.APIKeysSchema)
def get_api_keys(
    settings: Settings = Depends(get_settings),
):
    return s.APIKeysSchema(
        GOOGLE_CLIENT_ID=settings.GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET=settings.GOOGLE_CLIENT_SECRET,
    )
