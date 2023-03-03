from functools import lru_cache
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    # token
    JWT_SECRET: str = "<None>"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 4320
    # db
    DB_URI: str = ""

    # admin
    ADMIN_USER: str = "admin"
    ADMIN_PASS: str = "admin"
    ADMIN_EMAIL: EmailStr = "admin@admin.com"

    # Mail settings
    MAIL_USERNAME: str = "test_mail_username"
    MAIL_PASSWORD: str = "test_mail_password"
    MAIL_FROM: EmailStr = EmailStr("chairlift@simple2b.com")
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "test_mail_server"
    MAIL_FROM_NAME: str = "Chairlift"
    # Testing
    TEST_SEND_EMAIL: bool = False
    TEST_TARGET_EMAIL: str | None

    # STRIPE
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLIC_KEY: str = ""

    class Config:
        env_file = ".env"

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


@lru_cache
def get_settings() -> Settings:
    return Settings()
