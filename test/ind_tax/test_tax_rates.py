import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.tax_rates
class TestTaxRatesGet():
    # def test_list_success(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     # TODO: create project
    #     # TODO: create capsgen for new project
    #     response = get_req('/ind_tax/tax_rates?project_id=1', client, token)
    #     # TODO: delete project
    #
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'

    def test_list_fail(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/ind_tax/tax_rates', client, token)

        assert response.status_code == 400
        data = response.get_json()
        assert 'Error' in data['status']

    def test_list_no_project_fail(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/ind_tax/tax_rates?project_id=-1', client, token)

        assert response.status_code == 404
        data = response.get_json()
        assert 'Error' in data['status']

    # def test_list_caps_gen_fail(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     # TODO: create project
    #     response = get_req('/ind_tax/tax_rates?project_id=1', client, token)
    #     # TODO: delete project
    #
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'
    #     assert len(data['payload']) > 0
