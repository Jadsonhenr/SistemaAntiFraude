import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///antifraude-dev.db"
    )

    # Utiliza o driver psycopg 3 quando a conexão é PostgreSQL.
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = (
        int(os.getenv("MAX_CONTENT_LENGTH_MB", "100")) * 1024 * 1024
    )

    UPLOAD_MAX_FILES = int(os.getenv("UPLOAD_MAX_FILES", "500"))

    STORAGE_PATH = os.getenv(
        "STORAGE_PATH",
        str(Path("storage").resolve())
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    WTF_CSRF_TIME_LIMIT = None

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    DEBUG = os.getenv("FLASK_ENV") == "development"