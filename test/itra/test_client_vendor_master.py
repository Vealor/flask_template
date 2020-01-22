import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.client_vendor_master
class TestClientVendorMasterGet():
    # def test_get_client_vendor_master_success(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     response = get_req('/itra/client_vendor_master?project_id=1', client, token)
    #
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'

    def test_get_client_vendor_master_no_project_id(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/itra/client_vendor_master', client, token)

        assert response.status_code == 400
        data = response.get_json()
        assert 'Error' in data['status']
        assert data['message'] == 'Please specify a Project ID as an argument for the query.'

    def test_get_client_vendor_master_project_no_exist(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/itra/client_vendor_master?project_id=-1', client, token)

        assert response.status_code == 404
        data = response.get_json()
        assert 'Error' in data['status']
        assert data['message'] == 'Project does not exist.'

    # def test_get_client_vendor_master_project_no_capsgen(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     project_id = 1
    #     # create project
    #     response = get_req('/itra/client_vendor_master?project_id=' + str(project_id), client, token)
    #     # delete created project
    #
    #     assert response.status_code == 400
    #     data = response.get_json()
    #     assert 'Error' in data['status']
    #     assert data['message'] == 'There is no CapsGen for this project.'
