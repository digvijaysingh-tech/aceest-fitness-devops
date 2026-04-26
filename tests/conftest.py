import os

import pytest

from app import clients as clients_mod
from app import db as db_mod
from app.clients import ClientStore
from app.main import create_app


@pytest.fixture(autouse=True)
def _tmp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    db_mod.reset_initialized_cache()
    monkeypatch.setenv("ACEEST_DB_PATH", str(db_file))
    monkeypatch.setattr(db_mod, "DEFAULT_DB_PATH", str(db_file))
    monkeypatch.setattr(clients_mod, "store", ClientStore(str(db_file)))
    yield
    db_mod.reset_initialized_cache()


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c
