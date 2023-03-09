from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi import HTTPException, status
from jose import jwt

from app.config import get_settings
from app.database import get_db
from app.model import SuperUser
from app.oauth2 import create_access_token

db = get_db().__next__()
settings = get_settings()


class BaseAuthenticationBackend(AuthenticationBackend):
    async def login(
        self,
        request: Request,
        db=db,
    ) -> bool:
        form = await request.form()
        email = form["email"]
        password = form["password"]
        superuser = SuperUser.authenticate(db, email, password)  # type: ignore
        if not superuser:
            return False
        access_token = create_access_token(data={"user_id": superuser.id})
        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        token_data = jwt.decode(token, settings.JWT_SECRET)
        superuser: SuperUser = (
            db.query(SuperUser).filter_by(id=token_data["user_id"]).first()
        )
        if not superuser:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return True


authentication_backend: BaseAuthenticationBackend = BaseAuthenticationBackend(
    secret_key=settings.JWT_SECRET
)
