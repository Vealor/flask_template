import enum
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.types import Boolean, Date, DateTime, VARCHAR, Float, Integer, BLOB

db = SQLAlchemy()
ma = Marshmallow()

################################################################################
# ENUMS

class GlobalPermissions(enum.Enum):
    it_admin = "it_admin"

class ProjectPermissions(enum.Enum):
    tax_admin = "tax_admin"
    data_admin = "data_admin"
    tax_approver = "tax_approver"

class Actions(enum.Enum):
    create = "create"
    delete = "delete"
    modify = "modify"
    approve = "approve"


class Activity(enum.Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class Datatype(enum.Enum):
    dt_boolean = Boolean
    dt_date = Date
    dt_datetime = DateTime
    dt_varchar = VARCHAR
    dt_float = Float
    dt_int = Integer
    dt_blob = BLOB


################################################################################
# Many 2 Many links

user_global_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('global_permissions', db.Enum(GlobalPermissions), nullable=False, primary_key=True)
)

user_project_permissions = db.Table('user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('project_permissions', db.Enum(ProjectPermissions), nullable=False, primary_key=True)
)

################################################################################
# AUTH User and Token models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), unique = True, index = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    user_logs = db.relationship('Log', back_populates='log_user', lazy='dynamic')
    locked_transactions = db.relationship('Transaction', back_populates='locked_transaction_user', lazy='dynamic')
    user_projects = db.relationship('Project', secondary=user_project_permissions, lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'project_permission_map': []
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def superuser_exists(cls):
        return cls.query.filter_by(is_superuser=True).all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class BlacklistToken(db.Model):
    __tablename__ = 'blacklisted_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

################################################################################
# DATA Models

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    action = db.Column(db.Enum(Actions), nullable=False)
    affected_entity = db.Column(db.String(256), nullable=False)
    details = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_user = db.relationship('User', back_populates='user_logs')

    @property
    def serialize(self):
        username = ((User.query.filter_by(id=self.user_id).one()).serialize)['username']
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d_%H:%M:%S"),
            'action': self.action.value,
            'affected_entity': self.affected_entity,
            'details': self.details,
            'user_id': self.user_id,
            'username': username
        }

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    client_industry = db.relationship('Industry', back_populates='industry_clients')

    client_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_client', cascade="save-update", lazy='dynamic')
    client_projects = db.relationship('Project', back_populates='project_client', cascade="save-update", lazy='dynamic')
    client_client_models = db.relationship('ClientModel', back_populates='client_model_client', cascade="save-update", lazy='dynamic')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'industry_id': self.industry_id
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()


class Industry(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    industry_clients = db.relationship('Client', back_populates='client_industry', lazy='dynamic')
    industry_paredown_rules = db.relationship('ParedownRule', back_populates='paredown_rule_industry', lazy='dynamic')
    industry_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_industry', lazy='dynamic')
    industry_industry_model = db.relationship('IndustryModel', back_populates='industry_model_industries', lazy='dynamic')

class ParedownRule(db.Model):
    # these rules are only either core, or for an industry
    # there are no project specific rules
    __tablename__ = 'paredown_rules'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id', ondelete='SET NULL'), server_default=None, nullable=True)
    paredown_rule_industry = db.relationship('Industry', back_populates='industry_paredown_rules')
    #TODO add in rule saving data

class ClassificationRule(db.Model):
    __tablename__ = 'classification_rules'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id', ondelete='SET NULL'), server_default=None, nullable=True)
    classification_rule_industry = db.relationship('Industry', back_populates='industry_classification_rules')

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='SET NULL'), server_default=None, nullable=True)
    classification_rule_client = db.relationship('Client', back_populates='client_classification_rules')
    #TODO add in rule saving data

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    is_approved = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_archived = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    project_client = db.relationship('Client', back_populates='client_projects')

    project_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_project', lazy='dynamic')
    project_transactions = db.relationship('Transaction', back_populates='transaction_project', lazy='dynamic')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_approved': self.is_approved,
            'is_archived': self.is_archived,
            'area': 'TBD',
            'code': 'TBD',
            'project': 'TBD'
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    vendor_transactions = db.relationship('Transaction', back_populates='transaction_vendor')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()


class DataMapping(db.Model):
    __tablename__ = 'data_mappings'
    column_name = db.Column(db.String(256), nullable=False)
    table_name = db.Column(db.String(256), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    data_mapping_project = db.relationship('Project', back_populates='project_data_mappings')

    cdm_label_script_label = db.Column(db.String(256), db.ForeignKey('cdm_labels.script_labels'), nullable=False, primary_key=True)
    data_mapping_cdm_label = db.relationship('CDM_label', back_populates='cdm_label_data_mappings')

class CDM_label(db.Model):
    __tablename__ = 'cdm_labels'
    script_labels = db.Column(db.String(256), primary_key=True, nullable=False)
    english_labels = db.Column(db.String(256), nullable=False)
    is_calculated = db.Column(db.Boolean, unique=False, nullable=False)
    is_required = db.Column(db.Boolean, unique=False, nullable=False)
    is_unique = db.Column(db.Boolean, unique=False, nullable=False)
    datatype = db.Column(db.Enum(Datatype), nullable=False)
    regex = db.Column(db.String(256), nullable=False)

    cdm_label_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_cdm_label', lazy='dynamic')

class ClientModel(db.Model):
    __tablename__ = 'client_models'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    status = db.Column(db.Enum(Activity), unique=False, server_default=Activity.pending.value, nullable=False)

    cliend_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    client_model_client = db.relationship('Client', back_populates='client_client_models')

    client_model_transactions = db.relationship('Transaction', back_populates='transaction_client_model', lazy='dynamic')
    client_model_model_performances = db.relationship('ClientModelPerformance', back_populates='performance_client_model', lazy='dynamic')

class ClientModelPerformance(db.Model):
    __tablename__ = 'client_model_performances'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    client_model_id = db.Column(db.Integer, db.ForeignKey('client_models.id', ondelete='CASCADE'))
    performance_client_model = db.relationship('ClientModel', back_populates='client_model_model_performances')

class IndustryModel(db.Model):
    __tablename__ = 'industry_models'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    status = db.Column(db.Enum(Activity), unique=False, server_default=Activity.pending.value, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id', ondelete='CASCADE'), nullable=False)
    industry_model_industries = db.relationship('Industry', back_populates='industry_industry_model')

    industry_model_transactions = db.relationship('Transaction', back_populates='transaction_industry_model', lazy='dynamic')
    industry_model_model_performances = db.relationship('IndustryModelPerformance', back_populates='performance_industry_model', lazy='dynamic')

class IndustryModelPerformance(db.Model):
    __tablename__ = 'industry_model_performances'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    industry_model_id = db.Column(db.Integer, db.ForeignKey('industry_models.id', ondelete='CASCADE'), nullable=False)
    performance_industry_model = db.relationship('IndustryModel', back_populates='industry_model_model_performances')

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    modified = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_required = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    rbc_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    rbc_recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    image = db.Column(db.LargeBinary, server_default=None, nullable=True)
    data = db.Column(postgresql.JSON, nullable=False)

    locked_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), server_default=None, nullable=True)
    locked_transaction_user = db.relationship('User', back_populates='locked_transactions')

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    transaction_vendor = db.relationship('Vendor', back_populates='vendor_transactions')

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    transaction_project = db.relationship('Project', back_populates='project_transactions')

    client_model_id = db.Column(db.Integer, db.ForeignKey('client_models.id', ondelete='SET NULL'), server_default=None, nullable=True)
    transaction_client_model = db.relationship('ClientModel', back_populates='client_model_transactions')

    industry_model_id = db.Column(db.Integer, db.ForeignKey('industry_models.id', ondelete='SET NULL'), server_default=None, nullable=True)
    transaction_industry_model = db.relationship('IndustryModel', back_populates='industry_model_transactions')




##
