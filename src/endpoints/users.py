'''
User Endpoints
'''
import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from psycopg2.errors import NotNullViolation
from sqlalchemy.exc import IntegrityError
from src.errors import DataConflictError, InputError, NotFoundError, UnauthorizedError
from src.models import db, Roles, User
from src.util import validate_request_data, create_log
from src.wrappers import has_permission, exception_wrapper

users = Blueprint('users', __name__)
#===============================================================================
# GET ALL USER
@users.route('/', defaults={'id': None}, methods=['GET'])
@users.route('/<int:id>', methods=['GET'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_users(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = User.query
    # ID filter
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('ID {} does not exist.'.format(id))
    # Set ORDER
    query = query.order_by('username')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize_proj for i in query.all()] if 'projects' in args.keys() else [i.serialize for i in query.all()]

    return jsonify(response)

#===============================================================================
# POST NEW USER
@users.route('/', methods=['POST'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def create_user():
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # input validation
    request_types = {
        'username': ['str'],
        'password': ['str'],
        'email': ['str'],
        'initials': ['str'],
        'first_name': ['str'],
        'last_name': ['str'],
        'role': ['str']
    }
    validate_request_data(data, request_types)
    # PASSWORD STRENGTH CHECKING
    if len(data['password']) < 8:
        raise InputError("Password length must be greater than 8.")
    if not any(x.isupper() for x in data['password']):
        raise InputError("Password must contain a capital letter.")
    if not any(x.lower() for x in data['password']):
        raise InputError("Password must contain a lowercase letter.")
    if not any(x.isdigit() for x in data['password']):
        raise InputError("Password must contain a number.")
    # Length checking
    if len(data['username']) < 1 or len(data['username']) > 64:
        raise InputError('Username must be greater than 1 character and no more than 64')
    if len(data['password']) < 8 or len(data['password']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')
    if len(data['email']) < 1 or len(data['email']) > 128:
        raise InputError('Password must be greater than 8 character and no more than 128')
    if not re.match(r".*\@.+(?:\..+)+", data['email']):
        raise InputError('E-mail must be of a valid e-mail format.')
    if len(data['initials']) < 1 or len(data['initials']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')
    if len(data['first_name']) < 1 or len(data['first_name']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')
    if len(data['last_name']) < 1 or len(data['last_name']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')

    # check if this username exists
    check = User.query.filter_by(username=data['username']).first()
    if check:
        raise InputError('Username {} already exists.'.format(data['username']))
    # check if this email exists
    check = User.query.filter_by(email=data['email']).first()
    if check:
        raise InputError('User email {} already exists.'.format(data['email']))
    # check if these initials exist
    check = User.query.filter_by(initials=data['initials']).first()
    if check:
        raise InputError('User initials {} already exist.'.format(data['initials']))

    # ENUM check
    if data['role'] not in Roles.__members__:
        raise InputError('Specified role does not exists')

    # SYSTEM ADMIN CHECK
    # TODO: CHECK IF USER IS SUPERUSER (AKA LH GVA)
    is_sysadmin = False
    if 'is_system_administrator' in data.keys():
        is_sysadmin = bool(data['is_system_administrator'])

    # INSERT user
    new_user = User(
        username = data['username'],
        password = User.generate_hash(data['password']),
        email = data['email'],
        initials = data['initials'].upper(),
        first_name = data['first_name'],
        last_name = data['last_name'],
        role = data['role'],
        is_system_administrator = is_sysadmin
    )
    db.session.add(new_user)
    db.session.flush()

    db.session.commit()
    response['message'] = 'Created user {}'.format(data['username'])
    response['payload'] = [User.find_by_id(new_user.id).serialize]
    create_log(current_user, 'modify', 'User created a new User', 'New Username: ' + str(data['username']))

    return jsonify(response), 201

#===============================================================================
# UPDATE A USER information
@users.route('/<int:id>', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def update_user(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # input validation
    request_types = {
        'username': ['str'],
        'email': ['str'],
        'initials': ['str'],
        'first_name': ['str'],
        'last_name': ['str'],
        'role': ['str']  # TODO: if user does not have correct role, do not do this
    }
    validate_request_data(data, request_types)

    if len(data['username']) < 1 or len(data['username']) > 64:
        raise InputError('Username must be greater than 1 character and no more than 64')
    if len(data['email']) < 1 or len(data['email']) > 128:
        raise InputError('Password must be greater than 8 character and no more than 128')
    if not re.match(r".*\@.+(?:\..+)+", data['email']):
        raise InputError('E-mail must be of a valid e-mail format.')
    if len(data['initials']) < 1 or len(data['initials']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')
    if len(data['first_name']) < 1 or len(data['first_name']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')
    if len(data['last_name']) < 1 or len(data['last_name']) > 128:
        raise InputError('Password must be greater than 1 character and no more than 128')

    # UPDATE user
    query = User.find_by_id(id)
    if not query:
        raise NotFoundError('User ID {} does not exist.'.format(id))

    # check if data already exists
    check = User.query.filter_by(username=data['username']).filter(User.id != id).first()
    if check:
        raise InputError('Username {} already exists.'.format(data['username']))
    # check if this email exists
    check = User.query.filter_by(email=data['email']).filter(User.id != id).first()
    if check:
        raise InputError('User email {} already exists.'.format(data['email']))
    # check if these initials exist
    check = User.query.filter_by(initials=data['initials']).filter(User.id != id).first()
    if check:
        raise InputError('User initials {} already exist.'.format(data['initials']))

    # update user data
    query.username = data['username']
    query.email = data['email']
    query.initials = data['initials'].upper()
    query.first_name = data['first_name']
    query.last_name = data['last_name']
    if data['role'] not in Roles.__members__:
        raise InputError('Specified role does not exists')
    query.role = data['role']

    db.session.commit()
    response['message'] = 'Updated user with id {}'.format(id)
    response['payload'] = [User.find_by_id(id).serialize]
    create_log(current_user, 'modify', 'User updated a User', 'Updated Username: ' + str(data['username']))

    return jsonify(response), 201

#===============================================================================
# Check A USER password
@users.route('/<int:id>/passcheck', methods=['POST'])
@jwt_required
@exception_wrapper
def check_password(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # input validation
    request_types = {
        'password': ['str']
    }
    validate_request_data(data, request_types)

    query = User.find_by_id(id)
    if not User.verify_hash(data['password'], query.password):
        raise UnauthorizedError("Password Invalid")

    response['message'] = 'Password Valid'

    return jsonify(response), 200

#===============================================================================
# UPDATE A USER password
@users.route('/<int:id>/passchange', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def update_user_password(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # input validation
    request_types = {
        'password': ['str'],
        'newpassword': ['str'],
    }
    validate_request_data(data, request_types)

    # PASSWORD STRENGTH CHECKING
    if len(data['newpassword']) < 8:
        raise InputError("Password length must be greater than 8.")
    if not any(x.isupper() for x in data['newpassword']):
        raise InputError("Password must contain a capital letter.")
    if not any(x.lower() for x in data['newpassword']):
        raise InputError("Password must contain a lowercase letter.")
    if not any(x.isdigit() for x in data['newpassword']):
        raise InputError("Password must contain a number.")

    query = User.find_by_id(id)
    if not User.verify_hash(data['password'], query.password):
        raise UnauthorizedError("Password Invalid")

    query.password = User.generate_hash(data['newpassword'])
    query.req_pass_reset = False

    db.session.commit()
    response['message'] = 'Password changed'
    create_log(current_user, 'modify', 'User changed password for User', 'ID: ' + str(id))

    return jsonify(response), 201

#===============================================================================
# ACTIVATE A USER
@users.route('/<int:id>/activate', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def activate_user(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

    query = User.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('User ID {} does not exist.'.format(id))

    if query.is_active:
        response['message'] = 'User id {} is already active'.format(id)
    else:
        response['message'] = 'Activated user id {}'.format(id)
        query.is_active = True
        db.session.commit()
    response['payload'] = [query.serialize]
    create_log(current_user, 'modify', 'User activated a User', 'ID: ' + str(id))

    return jsonify(response), 200

#===============================================================================
# DEACTIVATE A USER
@users.route('/<int:id>/deactivate', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def deactivate_user(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

    if id == current_user.id:
        raise DataConflictError('You can not deactivate yourself.')

    query = User.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('User ID {} does not exist.'.format(id))

    if not query.is_active:
        response['message'] = 'User id {} is already deactivated'.format(id)
    else:
        response['message'] = 'Deactivated user id {}'.format(id)
        query.is_active = False
        db.session.commit()
    response['payload'] = [query.serialize]
    create_log(current_user, 'modify', 'User deactivated a User', 'ID: ' + str(id))

    return jsonify(response), 200

#===============================================================================
# DELETE A USER
@users.route('/<int:id>', methods=['DELETE'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def delete_user(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

    if id == current_user.id:
        raise DataConflictError('You can not delete yourself.')

    query = User.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('User ID {} does not exist.'.format(id))
    try:
        user = query.serialize
        db.session.delete(query)
        db.session.commit()
    except IntegrityError as e:
        assert isinstance(e.orig, NotNullViolation)
        raise DataConflictError('User can not be deleted because they have system data tied to their account. Please try deactivating the user instead.')

    response['message'] = 'Deleted user id {}'.format(id)
    response['payload'] = [user]
    create_log(current_user, 'modify', 'User deleted a User', 'Username: ' + str(user['username']))

    return jsonify(response), 200
