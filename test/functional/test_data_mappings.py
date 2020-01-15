import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.data_mappings
class TestDataMappingsGet():
    # def test_list_caps_gen_success(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     # TODO: make new caps_gen with data mappings
    #     response = get_req('/data_mappings?caps_gen_id=' + str(id), client, token)
    #
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'
    #     assert 'VERSION' in data.keys()

    def test_list_caps_gen_fail(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/data_mappings', client, token)

        assert response.status_code == 400
        data = response.get_json()
        assert 'Error' in data['status']

    # def test_list_single_success(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     response = get_req('/data_mappings', client, token)
    #
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'
    #     assert 'VERSION' in data.keys()

    def test_list_single_fail(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/data_mappings/-1', client, token)

        assert response.status_code == 404
        data = response.get_json()
        assert 'Error' in data['status']
