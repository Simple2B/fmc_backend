import boto3
from app.config import get_settings

settings = get_settings()

s3 = boto3.resource("s3")
session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)
s3 = session.resource("s3")
