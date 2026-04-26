import pytest

from app.clients import store
from app.main import create_app


@pytest.fixture(autouse=True)
def _reset_store():
    store.clear()
    yield
    store.clear()


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c
