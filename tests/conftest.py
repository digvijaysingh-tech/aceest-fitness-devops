import os

import pytest

from app import auth as auth_mod
from app import clients as clients_mod
from app import db as db_mod
from app import membership as membership_mod
from app import progress as progress_mod
from app import workouts as workouts_mod
from app.auth import UserStore
from app.clients import ClientStore
from app.main import create_app
from app.membership import MembershipStore
from app.progress import ProgressStore
from app.workouts import WorkoutStore


@pytest.fixture(autouse=True)
def _tmp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    db_mod.reset_initialized_cache()
    monkeypatch.setenv("ACEEST_DB_PATH", str(db_file))
    monkeypatch.setattr(db_mod, "DEFAULT_DB_PATH", str(db_file))
    monkeypatch.setattr(clients_mod, "store", ClientStore(str(db_file)))
    monkeypatch.setattr(progress_mod, "progress_store", ProgressStore(str(db_file)))
    monkeypatch.setattr(workouts_mod, "workout_store", WorkoutStore(str(db_file)))
    monkeypatch.setattr(membership_mod, "membership_store", MembershipStore(str(db_file)))
    monkeypatch.setattr(auth_mod, "user_store", UserStore(str(db_file)))
    yield
    db_mod.reset_initialized_cache()


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c
