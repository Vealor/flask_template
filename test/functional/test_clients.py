import pytest
from src import db
from src.models import Client
from test._helpers import login, get_req, post_req, put_req, delete_req
from test import api, client

@pytest.mark.clients
class TestClientGet():

    def test_client_get_one(self, api, client):

        # Test set-up
        db.session.add(Client(name = "Client One"))
        db.session.commit()
        new_client_id1 = Client.query.filter_by(name = "Client One").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/clients/' + str(new_client_id1), client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 1

        # Test clean up
        db.session.delete(Client.find_by_id(new_client_id1))
        db.session.commit()

    def test_client_get_all(self, api, client):

        # Test set-up
        db.session.add(Client(name = "Client One"))
        db.session.add(Client(name = "Client Two"))
        db.session.commit()
        new_client_id1 = Client.query.filter_by(name = "Client One").first().id
        new_client_id2 = Client.query.filter_by(name = "Client Two").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/clients', client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 2

        # Test clean up
        db.session.delete(Client.find_by_id(new_client_id1))
        db.session.delete(Client.find_by_id(new_client_id2))
        db.session.commit()

@pytest.mark.clients
class TestClientCreate():

    def test_client_create(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = post_req('/clients', client, {
            'name': "Client One",
            'client_entities': []
        }, helper_token)

        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0

        # Test clean up
        db.session.delete(Client.query.filter_by(name = "Client One").first())
        db.session.commit()

@pytest.mark.clients
class TestClientUpdate():

    def test_client_update(self, api, client):

        # Test set-up
        new_client = Client(name = "Client Two")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client Two").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = put_req('/clients/' + str(new_client_id), client, {
            'name': "Updated Client Two",
            'client_entities': []
        }, helper_token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0

        # Test clean up
        new_client = Client.find_by_id(new_client_id)
        db.session.delete(new_client)
        db.session.commit()


@pytest.mark.clients
class TestClientDelete():

    def test_client_delete(self, api, client):

        # Test set-up
        new_client = Client(name = "Client Three")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client Three").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = delete_req('/clients/' + str(new_client_id), client, helper_token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0
        assert Client.find_by_id(new_client_id) is None


# @pytest.mark.clients
# class TestInsufficientPermissionsDelete():

#     def test_client_delete_insuffperm(self, api, client):

#         # Test set-up
#         new_client = Client(name = "Client Four")
#         db.session.add(new_client)
#         db.session.commit()
#         new_client_id = Client.query.filter_by(name = "Client Four").first().id

#         # Test body
#         helper_token = login(client, 'wsmith', 'test')  # User with insuff. permissions
#         response = delete_req('/clients/' + str(new_client_id), client, helper_token)

#         assert response.status_code == 401
#         assert Client.find_by_id(new_client_id) is not None
