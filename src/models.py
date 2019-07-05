import enum
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql

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
    db.Column('globalpermission', db.Enum(GlobalPermissions), nullable=False)
)

user_project_permissions = db.Table('user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), nullable=False),
    db.Column('projectpermission', db.Enum(ProjectPermissions), nullable=False)
)

################################################################################
# AUTH User and Token models
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    username = db.Column(db.String(64), unique = True, index = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), nullable=False)

    logs = db.relationship('Logs', backref='users', lazy=True)
    locked_transactions = db.relationship('Transactions', backref='users', lazy=True)
    global_permissions = db.relationship('GlobalPermissions', secondary=user_global_permissions)
    project_permissions = db.relationship('ProjectPermissions', secondary=user_project_permissions)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class BlacklistTokens(db.Model):
    __tablename__ = 'blacklisted_tokens'
    id = db.Column(db.Integer, primary_key = True)
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

class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    action = db.Column(db.Enum(Actions), nullable=False)
    affected_entity = db.Column(db.String(256), nullable=False)
    details = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Industries(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    clients = db.relationship('Clients', backref='industries', lazy=True)
    paredown_rules = db.relationship('ParedownRules', backref='industries', lazy=True)
    classification_rules = db.relationship('ClassificationRules', backref='industries', lazy=True)
    industry_models = db.relationship('IndustryModel', backref='industries', lazy=True)

class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))

    classification_rules = db.relationship('ClassificationRules', backref='industries', lazy=True)
    projects = db.relationship('Projects', backref='clients', lazy=True)
    client_models = db.relationship('ClientModel', backref='clients', lazy=True)

class ParedownRules(db.Model):
    # these rules are only either core, or for an industry
    # there are no project specific rules
    __tablename__ = 'paredown_rules'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=True)
    # add in rule saving data

class ClassificationRules(db.Model):
    __tablename__ = 'classification_rules'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    # add in rule saving data

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    is_approved = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    is_archived = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    data_mappings = db.relationship('DataMappings', backref='projects', lazy=True)
    transactions = db.relationship('Transactions', backref='projects', lazy=True)

class Vendors(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    transactions = db.relationship('Transactions', backref='vendors', lazy=True)

class DataMappings(db.Model):
    __tablename__ = 'data_mappings'
    cdm_label = db.Column(db.Enum(CDM_Label), nullable=False, primary_key=True)
    column_name = db.Column(db.String(256), nullable=False)
    table_name = db.Column(db.String(256), nullable=False)
    is_required = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    is_unique = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    regex = db.Column(db.String(256), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, primary_key=True)


class ClientModel(db.Model):
    __tablename__ = 'client_model'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    cliend_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    client_model_performance = db.relationship('ClientModelPerformance', backref='client_model', lazy=True)

class ClientModelPerformance(db.Model):
    __tablename__ = 'client_model_performance'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    client_model_id = db.Column(db.Integer, db.ForeignKey('client_model.id'))

class IndustryModel(db.Model):
    __tablename__ = 'industry_model'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False, nullable=False)

    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)

    industry_model_performances = db.relationship('IndustryModelPerformance', backref='industry_model', lazy=True)

class IndustryModelPerformance(db.Model):
    __tablename__ = 'industry_model_performance'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    industry_model_id = db.Column(db.Integer, db.ForeignKey('industry_model.id'), nullable=False)

class Transasctions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    modified = db.Column(db.DateTime(timezone=True), nullable=True)
    is_required = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    is_predicted = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    recovery_probability = db.Column(db.Float, nullable=True)
    rbc_predicted = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    rbc_recovery_probability = db.Column(db.Float, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    data = db.Column(postgresql.JSON, nullable=False)

    locked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    client_model_id = db.Column(db.Integer, db.ForeignKey('client_model.id'), nullable=True)
    industry_model_id = db.Column(db.Integer, db.ForeignKey('industry_model.id'), nullable=True)





##
