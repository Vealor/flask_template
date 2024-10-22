# import pytest
# from test._helpers import login, get_req, post_req, put_req, delete_req
# from test import api, client
#
# @pytest.mark.auth
# class TestAuthReset():
#     def test_reset_success(self, api, client):
#         helper_token = login(client, 'base-admin', 'base-admin_pass')
#         new_user = post_req('/users', client, {
#             'username': 'authresettest',
#             'password': 'Authresettest123',
#             'email': 'authresettest@test.test',
#             'initials': 'test',
#             'first_name': 'test_first',
#             'last_name': 'test_last',
#             'role': 'admin'
#         }, helper_token)
#         assert new_user.status_code == 201
#         new_user_id = (new_user.get_json())['payload'][0]['id']
#         response = post_req('/auth/reset', client, {
#             'username': 'authresettest',
#             'email': 'authresettest@test.test'
#         })
#         del_new_user = delete_req('/users/' + str(new_user_id), client, helper_token)
#         assert del_new_user.status_code == 200
#
#         assert response.status_code == 201
#         data = response.get_json()
#         assert data['status'] == 'ok'
#         assert len(data['message']) > 0
#
#     def test_reset_fail(self, api, client):
#         response = post_req('/auth/reset', client, {
#             'username': 'authresettest-fail',
#             'email': 'lolnoemail@fail.fail'
#         })
#
#         assert response.status_code == 201
#         data = response.get_json()
#         assert data['status'] == 'ok'
#         assert len(data['message']) > 0
#
#
# @pytest.mark.auth
# class TestAuthLogin():
#     def test_login_success(self, api, client):
#         login_response = post_req('/auth/login', client, {
#             'username': 'base-admin',
#             'password': 'base-admin_pass'
#         })
#         assert login_response.status_code == 201
#         data = login_response.get_json()
#         assert data['status'] == 'ok'
#         assert len(data['message']) > 0
#         assert 'access_token' in data.keys()
#         assert len(data['access_token']) > 0
#         assert 'refresh_token' in data.keys()
#         assert len(data['refresh_token']) > 0
#
#     def test_login_fail(self, api, client):
#         login_response = post_req('/auth/login', client, {
#             'username': 'base-admin',
#             'password': 'password'
#         })
#         assert login_response.status_code == 401
#         data = login_response.get_json()
#         assert 'Error' in data['status']
#         assert data['message'] == "Wrong Credentials"
#         assert 'access_token' not in data.keys()
#         assert 'refresh_token' not in data.keys()
#
# @pytest.mark.auth
# class TestAuthRefresh():
#     def test_refresh_success(self, api, client):
#         login_response = post_req('/auth/login', client, {
#             'username': 'base-admin',
#             'password': 'base-admin_pass'
#         })
#         assert login_response.status_code == 201
#         token = (login_response.get_json())['refresh_token']
#         refresh = get_req('/auth/refresh', client, token)
#         assert refresh.status_code == 201
#         data = refresh.get_json()
#         assert data['status'] == 'ok'
#         assert 'access_token' in data.keys()
#         assert len(data['access_token']) > 0
#
# @pytest.mark.auth
# class TestAuthVerify():
#     def test_verify_success(self, api, client):
#         token = login(client, 'base-admin', 'base-admin_pass')
#         verify = get_req('/auth/verify', client, token)
#         assert verify.status_code == 200
#         data = verify.get_json()
#         assert data['status'] == 'ok'
#
# @pytest.mark.auth
# class TestAuthUserDetails():
#     def test_user_details_success(self, api, client):
#         token = login(client, 'base-admin', 'base-admin_pass')
#         verify = get_req('/auth/user_details', client, token)
#         assert verify.status_code == 200
#         data = verify.get_json()
#         assert data['status'] == 'ok'
#         assert 'id' in data['payload'].keys()
