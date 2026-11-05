import pytest
from app import create_app
from app.extensions import db

class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    STORAGE_PATH = "/tmp/antifraude-test-storage"
    UPLOAD_MAX_FILES = 20
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
