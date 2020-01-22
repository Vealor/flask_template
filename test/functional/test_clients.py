import pytest
from src import db
from src.models import Client, Project
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

    def test_client_get_one_does_not_exist(self, api, client):

        # Test set-up
        db.session.add(Client(name = "Client A"))
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client A").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/clients/' + str(new_client_id + 1), client, helper_token)
        assert response.status_code == 404  # NotFoundError
        data = response.get_json()
        assert data['payload'] == []

        # Test clean up
        db.session.delete(Client.find_by_id(new_client_id))
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

    def test_client_create_name_too_long(self, api, client):

        # Test set-up
        initial_count = Client.query.count()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = post_req('/clients', client, {
            'name': "Thisclientnameismuchtoolongforthedatabasetohandleallthecharactersinvolvedinitselfbutfirstoffwhywouldtheymakesuchastupidlylongnametobeginwith",
            'client_entities': []
        }, helper_token)

        assert response.status_code == 400  # InputError: Name too long
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.count() == initial_count  # Make sure no added entry in db

    def test_client_create_already_exists(self, api, client):

        # Test set-up
        new_client = Client(name = "Client B")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client B").first().id
        initial_count = Client.query.count()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = post_req('/clients', client, {
            'name': "Client B",
            'client_entities': []
        }, helper_token)

        assert response.status_code == 400  # InputError: Already exists
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.count() == initial_count  # Make sure no added entry in db

        # Test clean up
        db.session.delete(Client.find_by_id(new_client_id))
        db.session.commit()

    def test_client_create_valid_entity(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = post_req('/clients', client, {
            'name': "Client One",
            'client_entities': [{'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab', 'bc']}]
        }, helper_token)

        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0

        # Test clean up
        db.session.delete(Client.query.filter_by(name = "Client One").first())
        db.session.commit()

    def test_client_create_invalid_entity(self, api, client):

        # Test body
        # code is too long
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = post_req('/clients', client, {
            'name': "Bad Client",
            'client_entities': [{'company_code': 'CODE_IS_TOO_LONG', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab', 'bc']}]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Bad Client").count() == 0  # Make sure no entry in db

        # not recognized lob sector
        response = post_req('/clients', client, {
            'name': "Bad Client",
            'client_entities': [{'company_code': 'CODE', 'lob_sector': 'floral_industry_toilet_brushes', 'jurisdictions': ['on']}]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Bad Client").count() == 0  # Make sure no entry in db

        # no jurisdiction
        response = post_req('/clients', client, {
            'name': "Bad Client",
            'client_entities': [{'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': []}]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Bad Client").count() == 0  # Make sure no entry in db

        # same company code
        response = post_req('/clients', client, {
            'name': "Bad Client",
            'client_entities': [
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['bc']},
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab']}
            ]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Bad Client").count() == 0  # Make sure no entry in db

        # bad jurisdiction
        response = post_req('/clients', client, {
            'name': "Bad Client",
            'client_entities': [
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['tx']}
            ]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Bad Client").count() == 0  # Make sure no entry in db

        #duplicate jurisdiction
        response = post_req('/clients', client, {
            'name': "Bad Client",
            'client_entities': [
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab', 'ab']}
            ]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Bad Client").count() == 0  # Make sure no entry in db


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
            'client_entities': [{'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab']}]
        }, helper_token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0

        # Test clean up
        new_client = Client.find_by_id(new_client_id)
        db.session.delete(new_client)
        db.session.commit()

    def test_client_update_does_not_exist(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = put_req('/clients/' + str(1), client, {
            'name': "Client One",
            'client_entities': []
        }, helper_token)

        assert response.status_code == 404  # NotFoundError
        data = response.get_json()
        assert data['status'] == 'Error 404'
        assert data['payload'] == []

    def test_client_update_name_already_exists(self, api, client):

        # Test set-up
        new_client1 = Client(name = "Client One")
        new_client2 = Client(name = "Client Two")
        db.session.add(new_client1)
        db.session.add(new_client2)
        db.session.commit()
        new_client_id2 = Client.query.filter_by(name = "Client Two").first().id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = put_req('/clients/' + str(new_client_id2), client, {
            'name': "Client One",
            'client_entities': []
        }, helper_token)

        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []
        assert Client.query.filter_by(name = "Client One").count() == 1
        assert Client.query.filter_by(name = "Client Two").count() == 1

        # Test clean up
        db.session.delete(new_client1)
        db.session.delete(new_client2)
        db.session.commit()

    def test_client_update_invalid_entity(self, api, client):

        # Test set-up
        bad_client = Client(name = "Bad Client")
        db.session.add(bad_client)
        db.session.commit()
        bad_client_id = Client.query.filter_by(name = "Bad Client").first().id

        # Test body
        # code is too long
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = put_req('/clients/' + str(bad_client_id), client, {
            'name': "Bad Client",
            'client_entities': [{'company_code': 'CODE_IS_TOO_LONG', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab', 'bc']}]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []

        # not recognized lob sector
        response = put_req('/clients/' + str(bad_client_id), client, {
            'name': "Bad Client",
            'client_entities': [{'company_code': 'CODE', 'lob_sector': 'floral_industry_toilet_brushes', 'jurisdictions': ['on']}]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []

        # no jurisdiction
        response = put_req('/clients/' + str(bad_client_id), client, {
            'name': "Bad Client",
            'client_entities': [{'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': []}]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []

        # same company code
        response = put_req('/clients/' + str(bad_client_id), client, {
            'name': "Bad Client",
            'client_entities': [
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['bc']},
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab']}
            ]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []

        # bad jurisdiction
        response = put_req('/clients/' + str(bad_client_id), client, {
            'name': "Bad Client",
            'client_entities': [
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['tx']}
            ]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []

        #duplicate jurisdiction
        response = put_req('/clients/' + str(bad_client_id), client, {
            'name': "Bad Client",
            'client_entities': [
                {'company_code': 'CODE', 'lob_sector': 'business_services_business_services', 'jurisdictions': ['ab', 'ab']}
            ]
        }, helper_token)

        assert response.status_code == 400  # InputError
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert data['payload'] == []

        # Test cleanup
        db.session.delete(bad_client)
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

    def test_client_delete_fail_project_exists(self, api, client):

        # Test set-up
        new_client = Client(name = "Client C")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client C").first().id

        new_project = Project(name = "Project C", client_id = new_client_id, lead_partner_id = 2, lead_manager_id = 3)
        db.session.add(new_project)
        db.session.commit()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = delete_req('/clients/' + str(new_client_id), client, helper_token)

        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert len(data['payload']) == 0

        db.session.delete(new_project)
        db.session.delete(new_client)

    def test_client_delete_fail_client_dne(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = delete_req('/clients/' + str(23), client, helper_token)

        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'Error 404'
        assert len(data['payload']) == 0


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
