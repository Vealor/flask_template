import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.gst_registration
class TestGSTRegistrationGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/itra/gst_registration', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
