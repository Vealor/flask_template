import pytest
from test._helpers import login, get_req
from test import api, client

@pytest.mark.lob_sectors
class TestLOBSectorsGet():
    def test_list_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/core/lob_sectors', client, token)

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0
