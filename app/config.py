import os
from pathlib import Path

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///antifraude-dev.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "100")) * 1024 * 1024
    UPLOAD_MAX_FILES = int(os.getenv("UPLOAD_MAX_FILES", "500"))
    STORAGE_PATH = os.getenv("STORAGE_PATH", str(Path("storage").resolve()))
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    DEBUG = os.getenv("FLASK_ENV") == "development"
