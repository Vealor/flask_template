from test._helpers import login, get_req
from test import api, client

class TestCDMLabelsGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/cdm_labels', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0

    def test_caps_table_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/cdm_labels?caps_table', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0
