import pytest
from src import db
from src.models import Client, Project, CapsGen
from test._helpers import login, get_req
from test import api, client

@pytest.mark.tax_rates
class TestTaxRatesGet():
    # def test_list_success(self, api, client):
    #     token = login(client, 'lh-admin', 'Kpmg1234%')
    #     # TODO: create project
    #     # TODO: create capsgen for new project
    #     response = get_req('/tax_rates?project_id=1', client, token)
    #     # TODO: delete project
    #
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'

    def test_list_fail(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/tax_rates', client, token)

        assert response.status_code == 400
        data = response.get_json()
        assert 'Error' in data['status']

    def test_list_no_project_fail(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/tax_rates?project_id=-1', client, token)

        assert response.status_code == 404
        data = response.get_json()
        assert 'Error' in data['status']

    def test_list_caps_gen_fail(self, api, client):

        # Test set-up
        token = login(client, 'lh-admin', 'Kpmg1234%')

        new_client = Client(name = "Client A")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = new_client.id

        new_project = Project(name = "Project A", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
        db.session.add(new_project)
        db.session.commit()
        new_project_id = new_project.id

        # Test body
        response = get_req('/tax_rates?project_id=' + str(new_project_id), client, token)
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert len(data['payload']) == 0

        # Test clean up
        db.session.delete(Project.find_by_id(new_project_id))
        db.session.delete(Client.find_by_id(new_client_id))
        db.session.commit()

    def test_list_success(self, api, client):

        # Test set-up
        token = login(client, 'lh-admin', 'Kpmg1234%')

        new_client = Client(name = "Client A")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = new_client.id

        new_project = Project(name = "Project A", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
        db.session.add(new_project)
        db.session.commit()
        new_project_id = new_project.id

        new_caps_gen = CapsGen(project_id = new_project_id)
        db.session.add(new_caps_gen)
        db.session.commit()
        new_caps_gen_id = new_caps_gen.id

        # Test body
        response = get_req('/tax_rates?project_id=' + str(new_project_id), client, token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 0

        # Test clean up
        db.session.delete(CapsGen.find_by_id(new_caps_gen_id))
        db.session.delete(Project.find_by_id(new_project_id))
        db.session.delete(Client.find_by_id(new_client_id))
        db.session.commit()
