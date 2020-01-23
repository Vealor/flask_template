import pytest
from src import db
from src.ind_tax.models import FXRate
from test._helpers import login, get_req
from test import api, client

@pytest.mark.fx_rates
class TestFXRatesGet():
    def test_get_full_fresh_success(self, api, client):
        token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/ind_tax/fx_rates', client, token)

        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0

    def test_get_update_success(self, api, client):
        # fix this
        token = login(client, 'lh-admin', 'Kpmg1234%')
        rate = FXRate.query.order_by(FXRate.id.desc()).first()
        db.session.delete(rate)
        db.session.commit()
        response = get_req('/ind_tax/fx_rates', client, token)

        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) > 0
