# import pytest
# from test._helpers import login, get_req
# from test import api, client
#
# @pytest.mark.logs
# class TestLogsGet:
#     def test_list_success(self, api, client):
#         token = login(client, "base-admin", "base-admin_pass")
#         response = get_req("/logs", client, token)
#
#         assert response.status_code == 200
#         data = response.get_json()
#         assert data["status"] == "ok"
