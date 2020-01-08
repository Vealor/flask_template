from test._helpers import login, get_req
from test import api, client
from flask.testing import FlaskClient
import json
# content of test_class.py
class TestLogsGet():
    def test_one(self, api, client):
        token = login(client, 'lh-admin','Kpmg1234%')
        response = get_req('/logs', client, token)

        assert response.status_code == 200
        assert len(response.get_json()) > 0
