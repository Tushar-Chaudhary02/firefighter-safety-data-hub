import uuid
import boto3

from botocore.client import Config
from app.core.config import settings


def get_s3_client():
    if settings.FILE_STORAGE_BACKEND != "s3":
        raise RuntimeError("S3 is disabled; set FILE_STORAGE_BACKEND=s3 to enable it")

    if not settings.S3_BUCKET_NAME:
        raise RuntimeError("S3_BUCKET_NAME is required when FILE_STORAGE_BACKEND=s3")

    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )

    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        config=Config(signature_version="s3v4"),
    )


def build_s3_key(user_id: str, filename: str) -> str:
    unique = str(uuid.uuid4())
    return f"uploads/{user_id}/{unique}-{filename}"
