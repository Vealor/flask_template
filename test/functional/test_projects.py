import pytest
from src import db
from src.models import Client, Project
from test._helpers import login, get_req, post_req, put_req, delete_req
from test import api, client


#@pytest.mark.projects
# class TestProjectToggleFavourite():
#
#     def test_project_make_favourite(self, api, client):
#
#         # Test set-up
#         new_client = Client(name = "Client A")
#         db.session.add(new_client)
#         db.session.commit()
#         new_client_id = Client.query.filter_by(name = "Client B").first().id
#
#         new_project = Project(name = "Project A", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
#         db.session.add(new_project)
#         db.session.commit()
#         new_project_id = Project.query.filter_by(name = "Project B").first().id
#
#         # Test Body
#         helper_token = login(client, 'lh-admin', 'Kpmg1234%')
#         response = put_req('/projects/' + str(new_project_id) + '/toggle_favourite/', client, helper_token)
#
#         assert response.status_code == 200
#         data = response.get_json()
#         assert data['status'] == 'ok'
#         assert len(data['payload']) == 1
#
#         # Test clean up
#         db.session.delete(new_project)
#         db.session.delete(new_client)
#         db.session.commit()


@pytest.mark.projects
class TestProjectGet():

    def test_project_get_one(self, api, client):

        # Test set-up
        new_client = Client(name = "Client B")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client B").first().id

        new_project = Project(name = "Project B", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
        db.session.add(new_project)
        db.session.commit()
        new_project_id = new_project.id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/projects/' + str(new_project_id), client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 1

        # Test clean up
        db.session.delete(Project.find_by_id(new_project_id))
        db.session.delete(Client.find_by_id(new_client_id))
        db.session.commit()

    def test_project_get_all(self, api, client):

        # Test set-up
        new_client = Client(name = "Client A")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client A").first().id

        new_project = Project(name = "Project A", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
        db.session.add(new_project)
        db.session.commit()
        new_project_id_a = Project.query.filter_by(name = "Project A").first().id

        new_project = Project(name = "Project B", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
        db.session.add(new_project)
        db.session.commit()
        new_project_id_b = Project.query.filter_by(name = "Project B").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/projects', client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 2

        # Test clean up
        db.session.delete(Project.find_by_id(new_project_id_a))
        db.session.delete(Project.find_by_id(new_project_id_b))
        db.session.delete(Client.find_by_id(new_client_id))
        db.session.commit()

    def test_project_get_one_does_not_exist(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/projects/23', client, helper_token)
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'Error 404'
        assert len(data['payload']) == 0

# @pytest.mark.projects
# class TestProjectCreate():
#
#     def test_project_create(self, api, client):
#
#         # Test set-up
#         new_client = Client(name = "Client C")
#         db.session.add(new_client)
#         db.session.commit()
#         new_client_id = new_client.id
#
#         # Test body
#         helper_token = login(client, 'lh-admin', 'Kpmg1234%')
#         response = post_req('/projects/', client, {
#             'name': "Project C",
#             'client_id': new_client_id,
#             'lead_partner_id': 2,
#             'lead_manager_id': 3,
#             'project_users': [],
#             'tax_scope': {},
#             'engagement_scope': {}
#         }, helper_token)
#         print(response.get_json())
#         assert response.status_code == 200
#         data = response.get_json()
#         assert data['status'] == 'ok'
#         new_project_id = data['payload']['id]']
#         assert len(data['payload']) == 1
#
#         # Test clean up
#         db.session.delete(Project.find_by_id(new_project_id))
#         db.session.delete(Client.find_by_id(new_client_id))
#         db.session.commit()
