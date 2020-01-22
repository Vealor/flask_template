import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.logs
class TestLogsGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/core/logs', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
