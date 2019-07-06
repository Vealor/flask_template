import enum
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

db = SQLAlchemy()
ma = Marshmallow()

################################################################################
# ENUMS

class GlobalPermissions(enum.Enum):
    it_admin = "IT Admin"

class ProjectPermissions(enum.Enum):
    tax_admin = "Tax Admin"
    data_admin = "Data Admin"
    tax_approver = "Tax Approver"

class Actions(enum.Enum):
    create = "CREATE"
    delete = "DELETE"
    modify = "MODIFY"
    approve = "APPROVE"

class CDM_Label(enum.Enum):
    potato = "POTATO"

################################################################################
# Many 2 Many links

user_global_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('global_permissions', db.Enum(GlobalPermissions), nullable=False)
)

user_project_permissions = db.Table('user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), nullable=False),
    db.Column('project_permissions', db.Enum(ProjectPermissions), nullable=False)
)

################################################################################
# AUTH User and Token models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), unique = True, index = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    user_logs = db.relationship('Log', back_populates='log_user')
    locked_transactions = db.relationship('Transaction', back_populates='locked_transaction_user')

    # global_permissions = db.relationship('GlobalPermissions', secondary=user_global_permissions, back_populates='users')
    user_projects = db.relationship('Project', secondary=user_project_permissions)

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

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    client_industry = db.relationship('Industry', back_populates='industry_clients')

    client_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_client')
    client_projects = db.relationship('Project', back_populates='project_client')
    client_client_model = db.relationship('ClientModel', back_populates='client_model_clients')

class Industry(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    industry_clients = db.relationship('Client', back_populates='client_industry')
    industry_paredown_rules = db.relationship('ParedownRule', back_populates='paredown_rule_industry')
    industry_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_industry')
    industry_industry_model = db.relationship('IndustryModel', back_populates='industry_model_industries')

class ParedownRule(db.Model):
    # these rules are only either core, or for an industry
    # there are no project specific rules
    __tablename__ = 'paredown_rules'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=True)
    paredown_rule_industry = db.relationship('Industry', back_populates='industry_paredown_rules')
    #TODO add in rule saving data

class ClassificationRule(db.Model):
    __tablename__ = 'classification_rules'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=True)
    classification_rule_industry = db.relationship('Industry', back_populates='industry_classification_rules')

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    classification_rule_client = db.relationship('Client', back_populates='client_classification_rules')
    #TODO add in rule saving data

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    is_approved = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    is_archived = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    project_client = db.relationship('Client', back_populates='client_projects')

    project_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_project')
    project_transactions = db.relationship('Transaction', back_populates='transaction_project')

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    vendor_transactions = db.relationship('Transaction', back_populates='transaction_vendor')

class DataMapping(db.Model):
    __tablename__ = 'data_mappings'
    cdm_label = db.Column(db.Enum(CDM_Label), nullable=False, primary_key=True)
    column_name = db.Column(db.String(256), nullable=False)
    table_name = db.Column(db.String(256), nullable=False)
    is_required = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    is_unique = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    regex = db.Column(db.String(256), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, primary_key=True)
    data_mapping_project = db.relationship('Project', back_populates='project_data_mappings')

class ClientModel(db.Model):
    __tablename__ = 'client_models'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    cliend_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client_model_clients = db.relationship('Client', back_populates='client_client_model')

    client_model_transactions = db.relationship('Transaction', back_populates='transaction_client_model')
    client_model_model_performances = db.relationship('ClientModelPerformance', back_populates='performance_client_model')

class ClientModelPerformance(db.Model):
    __tablename__ = 'client_model_performances'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    client_model_id = db.Column(db.Integer, db.ForeignKey('client_models.id'))
    performance_client_model = db.relationship('ClientModel', back_populates='client_model_model_performances')

class IndustryModel(db.Model):
    __tablename__ = 'industry_models'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)
    industry_model_industries = db.relationship('Industry', back_populates='industry_industry_model')

    industry_model_transactions = db.relationship('Transaction', back_populates='transaction_industry_model')
    industry_model_model_performances = db.relationship('IndustryModelPerformance', back_populates='performance_industry_model')

class IndustryModelPerformance(db.Model):
    __tablename__ = 'industry_model_performances'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    industry_model_id = db.Column(db.Integer, db.ForeignKey('industry_models.id'), nullable=False)
    performance_industry_model = db.relationship('IndustryModel', back_populates='industry_model_model_performances')

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    modified = db.Column(db.DateTime(timezone=True), nullable=True)
    is_required = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    is_predicted = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    recovery_probability = db.Column(db.Float, nullable=True)
    rbc_predicted = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    rbc_recovery_probability = db.Column(db.Float, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    data = db.Column(postgresql.JSON, nullable=False)

    locked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    locked_transaction_user = db.relationship('User', back_populates='locked_transactions')

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    transaction_vendor = db.relationship('Vendor', back_populates='vendor_transactions')

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    transaction_project = db.relationship('Project', back_populates='project_transactions')

    client_model_id = db.Column(db.Integer, db.ForeignKey('client_models.id'), nullable=True)
    transaction_client_model = db.relationship('ClientModel', back_populates='client_model_transactions')

    industry_model_id = db.Column(db.Integer, db.ForeignKey('industry_models.id'), nullable=True)
    transaction_industry_model = db.relationship('IndustryModel', back_populates='industry_model_transactions')




##
