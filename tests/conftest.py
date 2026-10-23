import pytest
from database import db as db_module
from app import app as flask_app


@pytest.fixture
def app(tmp_path):
    db_path = str(tmp_path / "test.db")
    original_db_path = db_module.DB_PATH
    db_module.DB_PATH = db_path
    flask_app.config["TESTING"] = True
    with flask_app.app_context():
        db_module.init_db()
        db_module.seed_db()
    yield flask_app
    db_module.DB_PATH = original_db_path


@pytest.fixture
def client(app):
    return app.test_client()
