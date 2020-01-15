import pytest
from ._helpers import seed_db_data
from src import build_api, db

@pytest.fixture(scope="module")
def api(request):
    api = build_api()
    with api.app_context():
        if not request.config.getoption('--nodb'):
            print('\n\033[35mDROPPING DATABASE AND RESEED\033[0m\n')
            db.drop_all()
            db.create_all()
            seed_db_data()
        else:
            print('\n\033[33mDatabase Not Dropped\033[0m\n')

        yield api
        db.session.remove()

@pytest.fixture(scope="function")
def client(api):
    with api.test_client() as c:
        yield c
