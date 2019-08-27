'''
Client Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

clients = Blueprint('clients', __name__)
#===============================================================================
# GET ALL CLIENT
@clients.route('/', defaults={'id':None}, methods=['GET'])
@clients.route('/<path:id>', methods=['GET'])
# @jwt_required
def get_clients(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = Client.query

        # ID filter
        if id is not None:
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError('ID {} does not exist.'.format(id))
        # Set ORDER
        query = query.order_by('name')
        # Set LIMIT
        query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
        # Set OFFSET
        query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

        response['message'] = ''
        response['payload'] = [i.serialize for i in query.all()]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# POST NEW CLIENT
@clients.route('/', methods=['POST'])
# @jwt_required
def post_client():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'client_entities': 'list'
        }
        validate_request_data(data, request_types)
        client_entity_types = {
            'company_code': 'str',
            'lob_sector': 'str',
            'jurisdictions': 'list'
        }
        for entity in data['client_entities']:
            validate_request_data(entity, client_entity_types)

        # check if this name exists
        check = Client.query.filter_by(name=data['name']).first()
        if check:
            raise ValueError('Client {} already exists.'.format(data['name']))

        new_client = Client(
            name = data['name']
        )
        db.session.add(new_client)
        db.session.flush()

        for entity in data['client_entities']:
            if entity['lob_sector'] not in LineOfBusinessSectors.__members__:
                raise ValueError('Specified line of business sector does not exists')
            if ClientEntity.query.filter_by(client_id=new_client.id).filter_by(company_code=entity['company_code']).first():
                raise ValueError('Duplicate company codes for a client cannot exist.')
            new_entity = ClientEntity(
                client_id=new_client.id,
                company_code=entity['company_code'],
                lob_sector=entity['lob_sector'],
            )
            db.session.add(new_entity)
            db.session.flush()
            for jurisdiction in entity['jurisdictions']:
                if jurisdiction not in Jurisdiction.__members__:
                    raise ValueError('Specified jurisdiction does not exist.')
                if ClientEntityJurisdiction.query.filter_by(client_entity_id=new_entity.id).filter_by(jurisdiction=jurisdiction).first():
                    raise ValueError('Duplicate jurisdictions for a client entity cannot exist.')
                new_jurisdiction = ClientEntityJurisdiction(
                    client_entity_id=new_entity.id,
                    jurisdiction=jurisdiction,
                )
                db.session.add(new_jurisdiction)
                db.session.flush()

        db.session.commit()
        response['message'] = 'Created client {}'.format(data['name'])
        response['payload'] = [Client.find_by_id(new_client.id).serialize]
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# UPDATE A CLIENT
@clients.route('/<path:id>', methods=['PUT'])
# @jwt_required
def update_client(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'client_entities': 'list'
        }
        validate_request_data(data, request_types)
        client_entity_types = {
            'id': 'int',
            'company_code': 'str',
            'lob_sector': 'str',
            'jurisdictions': 'list'
        }
        for entity in data['client_entities']:
            validate_request_data(entity, client_entity_types)

        # UPDATE transaction
        query = Client.find_by_id(id)
        if not query:
            raise ValueError('Client ID {} does not exist.'.format(id))

        # check if this name exists
        check = Client.query.filter_by(name=data['name']).filter(Client.id != id).first()
        if check:
            raise ValueError('Client name {} already exists.'.format(data['name']))

        # update client name
        query.name = data['name']

        # update client entities
        for entity in data['client_entities']:
            if entity['lob_sector'] not in LineOfBusinessSectors.__members__:
                raise ValueError('Specified line of business sector does not exists')
            client_entity = ClientEntity.find_by_id(entity['id'])
            if not client_entity:
                raise ValueError('Client entity with ID {} does not exist.'.format(entity['id']))
            if ClientEntity.query.filter_by(client_id=id).filter_by(company_code=entity['company_code']).filter(ClientEntity.id != entity['id']).first():
                raise ValueError('Duplicate company codes for a client cannot exist.')
            client_entity.company_code = entity['company_code']
            client_entity.lob_sector = entity['lob_sector']
            # validate new jurisdictions for entity
            for jurisdiction in entity['jurisdictions']:
                if jurisdiction not in Jurisdiction.__members__:
                    raise ValueError('Specified jurisdiction does not exist.')
            # create/delete jurisdictions for entity
            client_entity_jurisdictions = ClientEntityJurisdiction.query.filter_by(client_entity_id=entity['id']).all()
            jurisdictions_list = entity['jurisdictions']
            for cej in client_entity_jurisdictions:
                if cej.jurisdiction.name in jurisdictions_list:
                    jurisdictions_list.remove(cej.jurisdiction.name)
                else:
                    db.session.delete(cej)
            for jurisdiction in jurisdictions_list:
                if ClientEntityJurisdiction.query.filter_by(client_entity_id=entity['id']).filter_by(jurisdiction=jurisdiction).first():
                    raise ValueError('Duplicate jurisdictions for a client entity cannot exist.')
                new_jurisdiction = ClientEntityJurisdiction(
                    client_entity_id=entity['id'],
                    jurisdiction=jurisdiction,
                )
                db.session.add(new_jurisdiction)
                db.session.flush()

        db.session.commit()
        response['message'] = 'Updated client with id {}'.format(id)
        response['payload'] = [Client.find_by_id(id).serialize]
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# DELETE A CLIENT
@clients.route('/<path:id>', methods=['DELETE'])
# @jwt_required
def delete_client(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        query = Client.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Client ID {} does not exist.'.format(id))

        # fail delete if has projects, models, or classification_rules
        if query.client_projects.all() or query.client_client_models.all():
        # if query.client_projects.all() or query.client_classification_rules.all() or query.client_client_models.all():
            raise Exception('Client not deleted. Client has active projects, models, or classification rules.')

        client = query.serialize
        db.session.delete(query)
        db.session.commit()
        response['message'] = 'Deleted client id {}'.format(client['id'])
        response['payload'] = [client]
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
