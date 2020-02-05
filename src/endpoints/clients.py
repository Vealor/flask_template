'''
Client Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from src.errors import InputError, NotFoundError
from src.models import db, Client, ClientEntity, ClientEntityJurisdiction, Jurisdiction, LineOfBusinessSectors
from src.util import validate_request_data, create_log
from src.wrappers import has_permission, exception_wrapper

clients = Blueprint('clients', __name__)
#===============================================================================
# GET ALL CLIENT
@clients.route('/', defaults={'id': None}, methods=['GET'])
@clients.route('/<int:id>', methods=['GET'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_clients(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = Client.query
    # ID filter
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('ID {} does not exist.'.format(id))
    # Set ORDER
    query = query.order_by('name')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# POST NEW CLIENT
@clients.route('/', methods=['POST'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def post_client():
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # input validation
    request_types = {
        'name': ['str'],
        'client_entities': ['list']
    }
    validate_request_data(data, request_types)
    if len(data['name']) < 1 or len(data['name']) > 128:
        raise InputError('Name must be greater than 1 character and no more than 128')

    client_entity_types = {
        'company_code': ['str'],
        'lob_sector': ['str'],
        'jurisdictions': ['list']
    }
    for entity in data['client_entities']:
        validate_request_data(entity, client_entity_types)
        if len(entity['company_code']) < 1 or len(entity['company_code']) > 4:
            raise InputError('Company Code for entity must be greater than 1 character and no more than 4')

    # check if this name exists
    check = Client.query.filter_by(name=data['name']).first()
    if check:
        raise InputError('Client {} already exists.'.format(data['name']))

    new_client = Client(
        name = data['name']
    )
    db.session.add(new_client)
    db.session.flush()

    for entity in data['client_entities']:
        if len(entity['company_code']) > 4:
            raise InputError('Company Code cannot exceed 4 characters.')
        if entity['lob_sector'] not in LineOfBusinessSectors.__members__:
            raise InputError('Specified line of business sector does not exists')
        if not len(entity['jurisdictions']):
            raise InputError('All entities must have at least one jurisdiction.')
        if ClientEntity.query.filter_by(client_id=new_client.id).filter_by(company_code=entity['company_code']).first():
            raise InputError('Duplicate company codes for a client cannot exist.')
        new_entity = ClientEntity(
            client_id=new_client.id,
            company_code=entity['company_code'],
            lob_sector=entity['lob_sector'],
        )
        db.session.add(new_entity)
        db.session.flush()
        for jurisdiction in entity['jurisdictions']:
            if jurisdiction not in Jurisdiction.__members__:
                raise InputError('Specified jurisdiction does not exist.')
            if ClientEntityJurisdiction.query.filter_by(client_entity_id=new_entity.id).filter_by(jurisdiction=jurisdiction).first():
                raise InputError('Duplicate jurisdictions for a client entity cannot exist.')
            new_jurisdiction = ClientEntityJurisdiction(
                client_entity_id=new_entity.id,
                jurisdiction=jurisdiction,
            )
            db.session.add(new_jurisdiction)
            db.session.flush()

    db.session.commit()
    response['message'] = 'Created client {}'.format(data['name'])
    response['payload'] = [Client.find_by_id(new_client.id).serialize]
    create_log(current_user, 'create', 'User created new Client', 'Client ID & name: ' + str(new_client.id) + " " + str(data['name']))

    return jsonify(response), 201

#===============================================================================
# UPDATE A CLIENT
@clients.route('/<int:id>', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def update_client(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # input validation
    request_types = {
        'name': ['str'],
        'client_entities': ['list']
    }
    validate_request_data(data, request_types)
    client_entity_types = {
        'company_code': ['str'],
        'lob_sector': ['str'],
        'jurisdictions': ['list']
    }
    for entity in data['client_entities']:
        validate_request_data(entity, client_entity_types)

    # UPDATE transaction
    query = Client.find_by_id(id)
    if not query:
        raise NotFoundError('Client ID {} does not exist.'.format(id))

    # check if this name exists
    check = Client.query.filter_by(name=data['name']).filter(Client.id != id).first()
    if check:
        raise InputError('Client name {} already exists.'.format(data['name']))

    # update client name
    query.name = data['name']

    # delete old entities
    client_entity_ids = [i.id for i in query.client_client_entities.all()]
    payload_entity_ids = [i['id'] for i in data['client_entities'] if 'id' in i.keys()]
    for payload_id in payload_entity_ids:
        if payload_id in client_entity_ids:
            client_entity_ids.remove(payload_id)
    for entity_id in client_entity_ids:
        db.session.delete(ClientEntity.find_by_id(entity_id))

    # update and add client entities
    for entity in data['client_entities']:

        # validate LoB for entity
        if entity['lob_sector'] not in LineOfBusinessSectors.__members__:
            raise InputError('Specified line of business sector does not exists')

        # validate new jurisdictions for entity
        for jurisdiction in entity['jurisdictions']:
            if jurisdiction not in Jurisdiction.__members__:
                raise InputError('Specified jurisdiction does not exist.')

        # validate company code length
        if len(entity['company_code']) > 4:
            raise InputError('Company Code cannot exceed 4 characters.')

        # validate has at least 1 jurisdiction for each entity
        if not len(entity['jurisdictions']):
            raise InputError('All entities must have at least one jurisdiction.')

        # update existing entity
        if 'id' in entity.keys() and entity['id'] is not None:
            client_entity = ClientEntity.find_by_id(entity['id'])
            if not client_entity:
                raise InputError('Client entity with ID {} does not exist.'.format(entity['id']))
            # check for duplicate compnay
            if ClientEntity.query.filter_by(client_id=id).filter_by(company_code=entity['company_code']).filter(ClientEntity.id != entity['id']).first():
                raise InputError('Duplicate company codes for a client cannot exist.')
            client_entity.company_code = entity['company_code']
            client_entity.lob_sector = entity['lob_sector']
        # build new entity
        else:
            if ClientEntity.query.filter_by(client_id=id).filter_by(company_code=entity['company_code']).first():
                raise InputError('Duplicate company codes for a client cannot exist.')

            new_client_entity = ClientEntity(
                client_id=id,
                company_code=entity['company_code'],
                lob_sector=entity['lob_sector'],
            )
            db.session.add(new_client_entity)
            db.session.flush()
            entity['id'] = new_client_entity.id

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
                raise InputError('Duplicate jurisdictions for a client entity cannot exist.')
            new_jurisdiction = ClientEntityJurisdiction(
                client_entity_id=entity['id'],
                jurisdiction=jurisdiction,
            )
            db.session.add(new_jurisdiction)
            db.session.flush()

    db.session.commit()
    response['message'] = 'Updated client with id {}'.format(id)
    response['payload'] = [Client.find_by_id(id).serialize]
    create_log(current_user, 'modify', 'User updated Client', 'Client ID & name: ' + str(id) + " " + str(data['name']))

    return jsonify(response), 200

#===============================================================================
# DELETE A CLIENT
@clients.route('/<int:id>', methods=['DELETE'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def delete_client(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

    query = Client.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('Client ID {} does not exist.'.format(id))

    # fail delete if has projects, models, or classification_rules
    # if query.client_projects.all() or query.client_classification_rules.all() or query.client_client_models.all():
    if query.client_projects.all() or query.client_client_models.all():
        raise InputError('Client not deleted. Client has active projects, models, or classification rules.')

    client = query.serialize
    db.session.delete(query)
    db.session.commit()
    response['message'] = 'Deleted client id {}'.format(client['id'])
    response['payload'] = [client]
    create_log(current_user, 'delete', 'User deleted Client', 'Client ID: ' + str(id))

    return jsonify(response), 200
