import pytest
# from ._helpers import seed_db_data
from src import build_api, db

@pytest.fixture(scope="session")
def api():
    api = build_api()
    with api.app_context():
        print("builing api")
        # db.drop_all()
        # db.create_all()
        # seed_db_data(db)

        yield api
        db.session.remove()

@pytest.fixture(scope="function")
def client(api):
    with api.test_client() as c:
        print("builing client")
        yield c
