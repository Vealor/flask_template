import pytest
from src import db
from src.models import User
from test._helpers import login, get_req, post_req, put_req, delete_req
from test import api, client

@pytest.mark.users
class TestUserGet():

    def test_users_get_one(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/users/1', client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 1

    def test_users_get_all(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/users/', client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 3

    def test_users_get_three(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/users?limit=3', client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 3

    def test_users_get_one_fail_dne(self, api, client):

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/users/90000', client, helper_token)
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'Error 404'
        assert len(data['payload']) == 0


@pytest.mark.users
class TestUserPost():

    def test_users_create_new_success(self, api, client):

        # Test set-up
        num_users_before = User.query.count()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        user_dict = {
            'username': 'my_username_z',
            'password': '1@cceptablePassword',
            'email': '123zfakestreet@hotmail.com',
            'initials': 'MRz',
            'first_name': "My",
            'last_name': "Realname",
            'role': "tax_practitioner"
        }
        response = post_req('/users/', client, user_dict, helper_token)
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 1
        assert num_users_before + 1 == User.query.count()

        # Test cleanup
        db.session.delete(User.find_by_id(int(data['payload'][0]['id'])))
        db.session.commit()

    def test_users_create_new_fail_password(self, api, client):

        # Test set-up
        num_users_before = User.query.count()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        user_dict = {
            'username': 'my_username_y',
            'password': '2short',
            'email': '123yfakestreet@hotmail.com',
            'initials': 'MRy',
            'first_name': "My",
            'last_name': "Realname",
            'role': "tax_practitioner"
        }
        response = post_req('/users/', client, user_dict, helper_token)
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert len(data['payload']) == 0
        assert num_users_before == User.query.count()

    def test_users_create_new_fail_role(self, api, client):

        # Test set-up
        num_users_before = User.query.count()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        user_dict = {
            'username': 'my_username_w',
            'password': User.generate_hash('2short'),
            'email': '123wfakestreet@hotmail.com',
            'initials': 'MR',
            'first_name': "My",
            'last_name': "Realname",
            'role': "my_own_job"
        }
        response = post_req('/users/', client, user_dict, helper_token)
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'Error 400'
        assert len(data['payload']) == 0
        assert num_users_before == User.query.count()

    def test_users_passcheck(self, api, client):

        # Test set-up
        user_dict = {
            'username': 'user_passcheck',
            'password': User.generate_hash('1@cceptablePassword'),
            'email': '123fake_users_passcheck@hotmail.com',
            'initials': 'MRxxx',
            'first_name': "My",
            'last_name': "Realname",
            'role': "tax_practitioner"
        }
        new_user = User(**user_dict)
        db.session.add(new_user)
        db.session.commit()
        new_user_id = new_user.id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')

        response = post_req('/users/' + str(new_user_id) + '/passcheck/', client, {'password': '2@cceptablepassword'}, helper_token)
        print(response.get_json()['message'])
        assert response.status_code == 401
        data = response.get_json()
        assert data['status'] == 'Error 401'

        response2 = post_req('/users/' + str(new_user_id) + '/passcheck/', client, {'password': '1@cceptablePassword'}, helper_token)
        print(response2.get_json())
        assert response2.status_code == 200
        data = response2.get_json()
        assert data['status'] == 'ok'

        # Test cleanup
        db.session.delete(User.find_by_id(new_user_id))
        db.session.commit()

@pytest.mark.users
class TestUserUpdate():

    def test_users_update_user(self, api, client):

        # Test set-up
        user_dict = {
            'username': 'my_username_a',
            'password': User.generate_hash('1Other@cceptablePassword'),
            'email': '123afakestreet@hotmail.com',
            'initials': 'MRa',
            'first_name': "My",
            'last_name': "Realname",
            'role': "tax_practitioner"
        }
        new_user = User(**user_dict)
        db.session.add(new_user)
        db.session.commit()
        new_user_id = new_user.id
        num_users_before = User.query.count()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        user_dict2 = {
            'username': 'my_username_b',
            'password': User.generate_hash('1Other@cceptablePassword'),
            'email': '321fakestreet@hotmail.com',
            'initials': 'MB',
            'first_name': "Myron",
            'last_name': "Bettername",
            'role': "tax_practitioner"
        }
        response = put_req('/users/' + str(new_user_id), client, user_dict2, helper_token)
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 1
        assert num_users_before == User.query.count()

        # Test cleanup
        db.session.delete(User.find_by_id(int(data['payload'][0]['id'])))
        db.session.commit()

    def test_users_passchange(self, api, client):

        # Test set-up
        user_dict = {
            'username': 'user_passcheck',
            'password': User.generate_hash('1OldPassword'),
            'email': '123fake_users_passcheck@hotmail.com',
            'initials': 'MRxxx',
            'first_name': "My",
            'last_name': "Realname",
            'role': "tax_practitioner"
        }
        new_user = User(**user_dict)
        db.session.add(new_user)
        db.session.commit()
        new_user_id = new_user.id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')

        response = put_req('/users/' + str(new_user_id) + '/passchange/', client, {'password': '1OldPassword', 'newpassword': 'invalidnewpass'}, helper_token)
        print(response.get_json()['message'])
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'Error 400'

        response = put_req('/users/' + str(new_user_id) + '/passchange/', client, {'password': '1WrongOldPassword', 'newpassword': '1NewPassword'}, helper_token)
        print(response.get_json()['message'])
        assert response.status_code == 401
        data = response.get_json()
        assert data['status'] == 'Error 401'

        response = put_req('/users/' + str(new_user_id) + '/passchange/', client, {'password': '1OldPassword', 'newpassword': '1NewPassword'}, helper_token)
        print(response.get_json())
        assert response.status_code == 201
        data = response.get_json()
        #assert data['status'] == 'ok'

        # Test cleanup
        db.session.delete(User.find_by_id(new_user_id))
        db.session.commit()
