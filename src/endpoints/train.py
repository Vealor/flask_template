'''
Train Endpoints
'''
import datetime
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import *
from src.util import get_date_obj_from_str, validate_request_data


train = Blueprint('train', __name__)

# ==============================================================================
# Specify the datatypes for the inputs to the train functionality


# ==============================================================================
# General
@train.route('/', methods=['POST'])
# @jwt_required
def do_train():
    response = {'status': '', 'message': '', 'payload': []}
    data = request.get_json()

    if request.method == 'POST':
        request_types = {
            'MODEL_TYPE': 'str',
            'CLIENT_ID': 'int',
            'TRAIN_DATA_START_DATE': 'str',
            'TRAIN_DATA_END_DATE': 'str',
            'TEST_DATA_START_DATE': 'str',
            'TEST_DATA_END_DATE': 'str'
            }
        try:
            # validate input
            validate_request_data(data, request_types)

            # check model type
            if data['MODEL_TYPE'] not in ['client', 'master']:
                raise ValueError('Specified model type `{}` is invalid'.format(data['MODEL_TYPE']))

            # validate date ranges
            train_start = get_date_obj_from_str(data['TRAIN_DATA_START_DATE'])
            train_end = get_date_obj_from_str(data['TRAIN_DATA_END_DATE'])
            test_start = get_date_obj_from_str(data['TEST_DATA_START_DATE'])
            test_end = get_date_obj_from_str(data['TEST_DATA_END_DATE'])
            if train_start >= train_end:
                raise ValueError('Invalid Train Data date range.')
            if test_start >= test_end:
                raise ValueError('Invalid Test Data date range.')
            if not (train_end < test_start or test_end < train_start):
                raise ValueError('Train and test data ranges overlap.')

            # At this point, all database independent checks have been perfrm'd
            # Now, database dependent checks begin
            if data['MODEL_TYPE'] == 'client':

                # Is the client id in the DATABASE?
                cid = data['CLIENT_ID']
                if not Client.find_by_id(cid):
                    raise ValueError('Client id \'{}\' is not in the database.'.format(cid))

                # Check if any projects exist for the client
                client_projects = [p.id for p in Project.query.filter_by(client_id = cid).distinct()]
                if len(client_projects) == 0:
                    raise ValueError('Client id \'{}\' has no projects in the database.'.format(cid))

                # Is there a pending client model? If so, STOP.
                if ClientModel.query.filter_by(client_id = cid).filter_by(status=Activity.pending.value).all():
                    raise Exception('There are pending models for this client.')

                # Are there sufficent transactions for training?
                transactions_count = Transaction.query.filter(Transaction.project_id.in_(client_projects)).filter_by(is_approved=True).count()
                if transactions_count < 6000:
                    raise Exception('Not enough data to train a client model. Only {} approved transactions.'.format(transactions_count))
            else:
                # Is there a pending master model? If so, STOP.
                if MasterModel.query.filter_by(status=Activity.pending.value).all():
                    raise Exception('There are pending master models.')

                # Are there sufficent transactions for training?
                if Transaction.query.filter_by(is_approved=True).count() < 10000:
                    raise Exception('Not enough data to train a master model. Only {} approved transactions.'.format(transactions_count))


        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400

        # ===================================================================
        # Now that all the database checks have been completed, we can submit
        # our request to the compute server

        model_data_dict = {
            'train_data_start': train_start,
            'train_data_end': train_end,
            'pickle': pickle.dumps(None),
            'hyper_p': {}
            }
        if input["MODEL_TYPE"] == 'client':
            # Create a placeholder entry in the model database to avoid multiple training instances
            cid = input['CLIENT_ID']
            model_data_dict['client_id'] = cid
            model_id = ClientModel(**model_data_dict).save_to_db()
            entry = ClientModel.query.filter_by(id=model_id).first()
            lh_model = client_model.ClientPredictionModel()
            client_projects = [p.id for p in Project.query.filter_by(client_id = cid).distinct()]
            transactions = Transaction.query.filter(Transaction.project_id.in_(client_projects))
        else:
            model_id = MasterModel(**model_data_dict).save_to_db()
            entry = MasterModel.query.filter_by(id=model_id).first()
            lh_model = master_model.MasterPredictionModel()
            transactions = Transaction.query

        # Try to train the instantiated model and edit the db entry
        try:
            transactions = transactions.filter_by(is_approved=True)
            entries = [i.serialize['data'] for i in transactions]
            df = pd.read_json('[' + ','.join(entries) + ']',orient='records')

            # Training ===============================================================
            # split into training and validation data and begin training
            data_train, data_valid = train_test_split(df,test_size=0.2,shuffle=True)
            data_train = preprocessing_train(data_train)


            target = "Target"
            predictors = list(set(data_train.columns) - set([target]))
            lh_model.train(data_train,predictors,target)

            # Update the model entry with the hyperparameters and pickle
            entry.pickle = lh_model.as_pickle()
            entry.hyper_p = {'predictors': predictors,
                             'target': target
                             }
            entry.update_to_db()

            # Output validation data results, used to assess model quality
            # Positive -> (Target == 1)
            data_valid = preprocessing_predict(data_valid,predictors,for_validation=True)
            performance_metrics = lh_model.validate(data_valid,predictors,target)
            model_performance_dict = {
                'accuracy': performance_metrics['accuracy'],
                'precision': performance_metrics['precision'],
                'recall': performance_metrics['recall'],
                'test_data_start': get_date_obj_from_str(input['TEST_DATA_START_DATE']),
                'test_data_end': get_date_obj_from_str(input['TEST_DATA_END_DATE'])
            }

        #If exception causes training failure...
        except Exception as e:

            # Remove the entry from the appropriate database
            entry.delete_from_db()

            # Send an email here?
            # ==================

            response['status'] = 'error'
            response['message'] = "Training failed: {}".format(str(e))
            return jsonify(response, 500)

        # Connect to the database and push trained model and performance metrics
        # to the appropriate entries.
        if input["MODEL_TYPE"] == 'client':
            model_performance_dict['client_model_id'] = model_id
            ClientModelPerformance(**model_performance_dict).save_to_db()
            # If there is no active model for this client, set it automatically to the current one.
            if not ClientModel.find_active_for_client(cid):
                ClientModel.set_active_for_client(model_id,cid)
        else:
            model_performance_dict['master_model_id'] = model_id
            MasterModelPerformance(**model_performance_dict).save_to_db()
            # If there is no active model, set the current one to be the active one.
            if not MasterModel.find_active():
                MasterModel.set_active(model_id)

        # Send an email here?
        # ==================

        # Send http response, terminate
        response['status'] = 'ok'
        response['payload']['performance_metrics'] = performance_metrics
        response['payload']['model_id'] = model_id
        response['payload']['model_type'] = input["MODEL_TYPE"]
        response['message'] = 'Model created, trained, and pushed to database. Notification sent to {}'.format('someone@kpmg.ca')
        return jsonify(response, 201)
