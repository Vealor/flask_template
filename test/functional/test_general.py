# import pytest
# from test._helpers import login, get_req
# from test import api, client
#
# @pytest.mark.general
# class TestGeneralGet:
#     def test_list_success(self, api, client):
#         token = login(client, "base-admin", "base-admin_pass")
#         response = get_req("/", client, token)
#
#         assert response.status_code == 200
#         data = response.get_json()
#         assert data["status"] == "ok"
#         assert "VERSION" in data.keys()  # test
