from datetime import datetime, timedelta
from jose import jwt
from app.config import Settings, get_settings

settings: Settings = get_settings()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET)

    return encoded_jwt
