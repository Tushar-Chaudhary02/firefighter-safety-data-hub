from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "local"
    APP_NAME: str = "Firefighter Safety Data Hub"
    API_V1_PREFIX: str = "/api/v1"

    # A clean checkout runs with SQLite and requires no external database.
    # PostgreSQL remains supported by overriding DATABASE_URL.
    DATABASE_URL: str = "sqlite:///./firefighter_local.db"

    SECRET_KEY: str = "local-development-secret-change-for-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 * 7

    CORS_ORIGINS: str = "*"

    # Console email is the local default. SES is opt-in for deployments.
    EMAIL_BACKEND: Literal["console", "ses"] = "console"
    SES_REGION: str = "us-east-1"
    SES_FROM_NAME: str = "Firefighter Data Hub"
    SES_FROM_EMAIL: str = "noreply@localhost"

    # Used for email verification tokens
    EMAIL_TOKEN_SECRET: str = "local-development-email-secret"

    # Current POC uses manual token entry in Flutter app.
    # Later you can switch to frontend link mode after public web frontend/domain exists.
    EMAIL_VERIFICATION_MODE: str = "manual"

    # Optional for later web verification links
    FRONTEND_VERIFY_BASE_URL: str | None = None
    WEB_FRONTEND_BASE_URL: str = "http://localhost:5173"

    # Local disk storage is the default; S3 is opt-in.
    FILE_STORAGE_BACKEND: Literal["local", "s3"] = "local"
    LOCAL_UPLOAD_DIR: str = "local_uploads"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None


settings = Settings()
