from test._helpers import login, get_req
from test import api, client

class TestLogsGet():
    def test_basic(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/logs', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0
