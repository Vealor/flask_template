import pickle
import pytest
from src import db
from src.util import get_date_obj_from_str
from src.models import Client, ClientModel
from test._helpers import login, get_req, post_req, put_req, delete_req
from test import api, client

@pytest.mark.client_models
class TestClientModelsGet():

    def test_client_model_get_one(self, api, client):

        # Test set-up

        new_client = Client(name = "Client A")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client A").first().id

        model_data_dict = {
            'client_id': new_client_id,
            'train_data_start': get_date_obj_from_str("2000-01-01"),
            'train_data_end': get_date_obj_from_str("2000-03-01"),
            'pickle': pickle.dumps(None),
            'hyper_p': {}
        }

        cm1 = ClientModel(**model_data_dict)
        cm2 = ClientModel(**model_data_dict)
        db.session.add(cm1)
        db.session.add(cm2)
        db.session.commit()
        cm1_id = cm1.id

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/client_models/' + str(cm1_id), client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 1

        # Test clean-up
        db.session.delete(cm1)
        db.session.delete(cm2)
        db.session.delete(new_client)
        db.session.commit()
        assert ClientModel.query.count() == 0
        assert Client.query.count() == 0

    def test_client_model_get_all(self, api, client):

        # Test set-up
        new_client = Client(name = "Client B")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client B").first().id

        model_data_dict = {
            'client_id': new_client_id,
            'train_data_start': get_date_obj_from_str("2000-01-01"),
            'train_data_end': get_date_obj_from_str("2000-03-01"),
            'pickle': pickle.dumps(None),
            'hyper_p': {}
        }

        cm1 = ClientModel(**model_data_dict)
        cm2 = ClientModel(**model_data_dict)
        db.session.add(cm1)
        db.session.add(cm2)
        db.session.commit()

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/client_models/', client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert len(data['payload']) == 2

        # Test clean-up
        db.session.delete(cm1)
        db.session.delete(cm2)
        db.session.delete(new_client)
        db.session.commit()
        assert ClientModel.query.count() == 0
        assert Client.query.count() == 0

    def test_client_model_get_status_training(self, api, client):

        # Test set-up
        new_client = Client(name = "Client C")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client C").first().id

        model_data_dict = {
            'client_id': new_client_id,
            'train_data_start': get_date_obj_from_str("2000-01-01"),
            'train_data_end': get_date_obj_from_str("2000-03-01"),
            'pickle': pickle.dumps(None),
            'hyper_p': {}
        }

        cm1 = ClientModel(**model_data_dict)
        db.session.add(cm1)
        db.session.commit()
        assert ClientModel.query.count() == 1

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/client_models/is_training?client_id={}'.format(new_client_id), client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['payload']['is_training'] is True

        # Test clean-up
        db.session.delete(cm1)
        db.session.delete(new_client)
        db.session.commit()
        assert ClientModel.query.count() == 0
        assert Client.query.count() == 0

    def test_client_model_get_status_pending(self, api, client):

        # Test set-up
        new_client = Client(name = "Client D")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client D").first().id

        model_data_dict = {
            'client_id': new_client_id,
            'train_data_start': get_date_obj_from_str("2000-01-01"),
            'train_data_end': get_date_obj_from_str("2000-03-01"),
            'pickle': pickle.dumps(None),
            'hyper_p': {}
        }

        cm1 = ClientModel(**model_data_dict)
        cm1.status = 'pending'
        db.session.add(cm1)
        db.session.commit()
        assert ClientModel.query.count() == 1

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = get_req('/client_models/has_pending?client_id={}'.format(new_client_id), client, helper_token)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['payload']['is_pending'] is True

        # Test clean-up
        db.session.delete(cm1)
        db.session.delete(new_client)
        db.session.commit()
        assert ClientModel.query.count() == 0
        assert Client.query.count() == 0

# @pytest.mark.client_models
# class TestClientModelsUpdate():
#
#     def test_client_model_set_active(self, api, client):
#
#         # Test set-up
#         new_client = Client(name = "Client E")
#         db.session.add(new_client)
#         db.session.commit()
#         new_client_id = Client.query.filter_by(name = "Client E").first().id
#
#         model_data_dict = {
#             'client_id': new_client_id,
#             'train_data_start': get_date_obj_from_str("2000-01-01"),
#             'train_data_end': get_date_obj_from_str("2000-03-01"),
#             'pickle': pickle.dumps(None),
#             'hyper_p': {}
#         }
#
#         cm1 = ClientModel(**model_data_dict)
#         db.session.add(cm1)
#         db.session.commit()
#         cm1_id = cm1.id
#         assert ClientModel.query.count() == 1
#
#         # Test body
#         helper_token = login(client, 'lh-admin', 'Kpmg1234%')
#         response = put_req('/client_models/' + str(cm1_id) + '/set_active/', client, {}, helper_token)
#         print(response.get_json())
#         assert response.status_code == 400
#         data = response.get_json()
#         assert data['status'] == 'Error 400'
#
#         cm1.status = 'pending'
#         db.session.add(cm1)
#         db.session.commit()
#
#         response2 = put_req('/client_models/' + str(cm1_id) + '/set_active/', client, {}, helper_token)
#         assert response2.status_code == 200
#         data = response2.get_json()
#         assert data['status'] == 'ok'
#
#         # Test clean-up
#         db.session.delete(cm1)
#         db.session.commit()
#         assert ClientModel.query.count() == 0

@pytest.mark.client_models
class TestClientModelsDelete():

    def test_client_model_delete(self, api, client):

        # Test set-up
        new_client = Client(name = "Client F")
        db.session.add(new_client)
        db.session.commit()
        new_client_id = Client.query.filter_by(name = "Client F").first().id

        model_data_dict = {
            'client_id': new_client_id,
            'train_data_start': get_date_obj_from_str("2000-01-01"),
            'train_data_end': get_date_obj_from_str("2000-03-01"),
            'pickle': pickle.dumps(None),
            'hyper_p': {}
        }

        cm1 = ClientModel(**model_data_dict)
        db.session.add(cm1)
        db.session.commit()
        cm1_id = cm1.id
        assert ClientModel.query.count() == 1

        # Test body
        helper_token = login(client, 'lh-admin', 'Kpmg1234%')
        response = delete_req('/client_models/9000', client, helper_token)
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'Error 404'

        response2 = delete_req('/client_models/' + str(cm1_id), client, helper_token)
        assert response2.status_code == 200
        data = response2.get_json()
        assert data['status'] == 'ok'
        assert ClientModel.query.count() == 0
