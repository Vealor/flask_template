import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.client_models
class TestClientModelsGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        # TODO: insert client
        # TODO: insert client_model
        response = get_req('/client_models', client, token)
        # TODO: delete client - hopefully cascades client_model

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        # assert len(data['payload']) > 0  # uncomment when TODOs above are done
