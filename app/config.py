from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    # token
    JWT_SECRET: str = "<None>"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 4320
    BASE_URL: str = "http://localhost:3000"
    COACH_DEFAULT_LESSON_PRICE: float = 999

    CONFIRMATION_URL_COACH: str
    CONFIRMATION_URL_STUDENT: str

    RESET_PASSWORD_URL_STUDENT: str
    RESET_PASSWORD_URL_COACH: str
    # db
    DB_URI: str = ""

    # admin
    ADMIN_USER: str = "admin"
    ADMIN_PASS: str = "admin"
    ADMIN_EMAIL: str = "admin@admin.com"

    # Mail settings
    MAIL_USERNAME: str = "test_mail_username"
    MAIL_PASSWORD: str = "test_mail_password"
    MAIL_FROM: str = "chairlift@simple2b.com"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "test_mail_server"
    MAIL_FROM_NAME: str = "Chairlift"
    # Testing
    TEST_SEND_EMAIL: bool = False
    TEST_TARGET_EMAIL: str | None

    # STRIPE
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLIC_KEY: str = ""

    # AWS
    AWS_SECRET_KEY: str
    AWS_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str = "find-my-coach"
    AWS_S3_BUCKET_URL: str

    GOOGLE_CLIENT_ID: str = "test_google_client_id"
    GOOGLE_CLIENT_SECRET: str = "test_google_client_secret"

    class Config:
        env_file = ".env"

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


@lru_cache
def get_settings() -> Settings:
    return Settings()
