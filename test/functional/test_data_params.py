from test._helpers import login, get_req
from test import api, client

class TestDataParamsGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/data_params?project_id=1', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
