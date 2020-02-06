import pickle
import pytest
from src import db
from src.util import get_date_obj_from_str
from src.models import Client, ClientModel
from test._helpers import login, get_req, post_req, put_req, delete_req
from test import api, client

@pytest.mark.client_models
class TestClientModelsGet():

    def test_master_model_get_one(self, api, client):

        # Test set-up

        db.session.add(Client(name = "Client A"))
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
        db.session.commit()

    # def test_master_model_get_all(self, api, client):
    #
    #     # Test set-up
    #     model_data_dict = {
    #         'train_data_start': get_date_obj_from_str("2000-01-01"),
    #         'train_data_end': get_date_obj_from_str("2000-03-01"),
    #         'pickle': pickle.dumps(None),
    #         'hyper_p': {}
    #     }
    #
    #     mm1 = MasterModel(**model_data_dict)
    #     mm2 = MasterModel(**model_data_dict)
    #     db.session.add(mm1)
    #     db.session.add(mm2)
    #     db.session.commit()
    #
    #     # Test body
    #     helper_token = login(client, 'lh-admin', 'Kpmg1234%')
    #     response = get_req('/master_models/', client, helper_token)
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'
    #     assert len(data['payload']) == 2
    #
    #     # Test clean-up
    #     db.session.delete(mm1)
    #     db.session.delete(mm2)
    #     db.session.commit()
    #     assert MasterModel.query.count() == 0
    #
    # def test_master_model_get_status_training(self, api, client):
    #
    #     # Test set-up
    #     model_data_dict = {
    #         'train_data_start': get_date_obj_from_str("2000-01-01"),
    #         'train_data_end': get_date_obj_from_str("2000-03-01"),
    #         'pickle': pickle.dumps(None),
    #         'hyper_p': {}
    #     }
    #
    #     mm1 = MasterModel(**model_data_dict)
    #     db.session.add(mm1)
    #     db.session.commit()
    #     assert MasterModel.query.count() == 1
    #
    #     # Test body
    #     helper_token = login(client, 'lh-admin', 'Kpmg1234%')
    #     response = get_req('/master_models/is_training/', client, helper_token)
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'
    #     assert data['payload']['is_training'] is True
    #
    #     # Test clean-up
    #     db.session.delete(mm1)
    #     db.session.commit()
    #     assert MasterModel.query.count() == 0
    #
    # def test_master_model_get_status_pending(self, api, client):
    #
    #     # Test set-up
    #     model_data_dict = {
    #         'train_data_start': get_date_obj_from_str("2000-01-01"),
    #         'train_data_end': get_date_obj_from_str("2000-03-01"),
    #         'pickle': pickle.dumps(None),
    #         'hyper_p': {}
    #     }
    #
    #     mm1 = MasterModel(**model_data_dict)
    #     mm1.status = 'pending'
    #     db.session.add(mm1)
    #     db.session.commit()
    #     assert MasterModel.query.count() == 1
    #
    #     # Test body
    #     helper_token = login(client, 'lh-admin', 'Kpmg1234%')
    #     response = get_req('/master_models/has_pending/', client, helper_token)
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert data['status'] == 'ok'
    #     assert data['payload']['is_pending'] is True
    #
    #     # Test clean-up
    #     db.session.delete(mm1)
    #     db.session.commit()
    #     assert MasterModel.query.count() == 0

# @pytest.mark.master_models
# class TestMasterModelsUpdate():
#
#     def test_master_model_set_active(self, api, client):
#
#         # Test set-up
#         model_data_dict = {
#             'train_data_start': get_date_obj_from_str("2000-01-01"),
#             'train_data_end': get_date_obj_from_str("2000-03-01"),
#             'pickle': pickle.dumps(None),
#             'hyper_p': {}
#         }
#
#         mm1 = MasterModel(**model_data_dict)
#         db.session.add(mm1)
#         db.session.commit()
#         mm1_id = mm1.id
#         assert MasterModel.query.count() == 1
#
#         # Test body
#         helper_token = login(client, 'lh-admin', 'Kpmg1234%')
#         response = put_req('/master_models/' + str(mm1_id) + '/set_active/', client, {}, helper_token)
#         print(response.get_json())
#         assert response.status_code == 400
#         data = response.get_json()
#         assert data['status'] == 'Error 400'
#
#         mm1.status = 'pending'
#         db.session.add(mm1)
#         db.session.commit()
#
#         response2 = put_req('/master_models/' + str(mm1_id) + '/set_active/', client, {}, helper_token)
#         assert response2.status_code == 200
#         data = response2.get_json()
#         assert data['status'] == 'ok'
#
#         # Test clean-up
#         db.session.delete(mm1)
#         db.session.commit()
#         assert MasterModel.query.count() == 0

# @pytest.mark.master_models
# class TestMasterModelsDelete():
#
#     def test_master_model_delete(self, api, client):
#
#         # Test set-up
#         model_data_dict = {
#             'train_data_start': get_date_obj_from_str("2000-01-01"),
#             'train_data_end': get_date_obj_from_str("2000-03-01"),
#             'pickle': pickle.dumps(None),
#             'hyper_p': {}
#         }
#
#         mm1 = MasterModel(**model_data_dict)
#         db.session.add(mm1)
#         db.session.commit()
#         mm1_id = mm1.id
#         assert MasterModel.query.count() == 1
#
#         # Test body
#         helper_token = login(client, 'lh-admin', 'Kpmg1234%')
#         response = delete_req('/master_models/9000', client, helper_token)
#         assert response.status_code == 404
#         data = response.get_json()
#         assert data['status'] == 'Error 404'
#
#         response2 = delete_req('/master_models/' + str(mm1_id), client, helper_token)
#         assert response2.status_code == 200
#         data = response2.get_json()
#         assert data['status'] == 'ok'
#         assert MasterModel.query.count() == 0
