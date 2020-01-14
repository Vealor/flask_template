from test._helpers import login, get_req
from test import api, client

class TestGeneralGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'VERSION' in data.keys()
