import boto3
from app.config import get_settings, Settings

settings = get_settings()


def create_s3_conn(settings: Settings):
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
    )
    s3 = session.client("s3")
    return s3
