import enum
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.types import Boolean, Date, DateTime, VARCHAR, Float, Integer, BLOB

db = SQLAlchemy()

################################################################################
# ENUMS

class Roles(enum.Enum):
    it_admin = "it_admin"
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

class Juristiction(enum.Enum):
    ab = "Alberta"
    bc = "British Columbia"
    mb = "Manitoba"
    nb = "New Brunswick"
    nl = "Newfoundland and Labrador"
    nt = "Northwest Territories"
    ns = "Nova Scotia"
    nu = "Nunavut"
    on = "Ontario"
    pe = "Prince Edward Island"
    qc = "Quebec"
    sk = "Saskatchewan"
    ty = "Yukon"
    foreign = "Outside Canada"

################################################################################
# Many 2 Many links

project_sector_link = db.Table('project_sector',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('sector_id', db.Integer, db.ForeignKey('sectors.id', ondelete='CASCADE'), nullable=False, primary_key=True)
)

user_project_link = db.Table('user_project',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('is_favourite', db.Boolean, unique=False, default=False, server_default='f', nullable=False)
)

################################################################################
# AUTH User and Token models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), unique = True, index = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    initials = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    req_pass_reset = db.Column(db.Boolean, unique=False, default=True, server_default='t', nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)

    user_projects = db.relationship('Project', secondary=user_project_link)
    user_logs = db.relationship('Log', back_populates='log_user', lazy='dynamic')
    locked_transactions = db.relationship('Transaction', back_populates='locked_transaction_user', lazy='dynamic')


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'initials': self.initials.upper(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': "{} {}".format(self.first_name, self.last_name),
            'req_pass_reset': self.req_pass_reset,
            'role': self.role.name,
            'user_projects': [i.serialize for i in self.user_projects]
        }

    @classmethod
    def superuser_exists(cls):
        return cls.query.filter_by(is_superuser=True).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

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
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    action = db.Column(db.Enum(Actions), nullable=False)
    affected_entity = db.Column(db.String(256), nullable=False)
    details = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, nullable=False) # FK
    log_user = db.relationship('User', back_populates='user_logs') # FK

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

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
    __table_args__ = (
        db.UniqueConstraint('name', 'line_of_business_id', name='client_unique_constraint'),
        db.ForeignKeyConstraint(['line_of_business_id'], ['line_of_business.id']),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    line_of_business_id = db.Column(db.Integer, nullable=False) # FK
    client_line_of_business = db.relationship('LineOfBusiness', back_populates='line_of_business_clients') # FK

    # client_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_client', cascade="save-update", lazy='dynamic')
    client_projects = db.relationship('Project', back_populates='project_client', cascade="save-update", lazy='dynamic')
    client_client_models = db.relationship('ClientModel', back_populates='client_model_client', cascade="save-update", lazy='dynamic')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return { 'name': self.name, 'line_of_business_id': self.line_of_business_id }

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
            'line_of_business_id': self.line_of_business_id,
            'client_line_of_business': self.client_line_of_business.name,
            'client_projects': [i.serialize for i in self.client_projects]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()


class LineOfBusiness(db.Model):
    __tablename__ = 'line_of_business'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    line_of_business_clients = db.relationship('Client', back_populates='client_line_of_business', lazy='dynamic')
    line_of_business_paredown_rules = db.relationship('ParedownRule', back_populates='paredown_rule_line_of_business', lazy='dynamic')
    # line_of_business_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_line_of_business', lazy='dynamic')
    line_of_business_sectors = db.relationship('Sector', back_populates='sector_line_of_business', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'line_of_business_sectors': [i.serialize for i in self.line_of_business_sectors],
            'line_of_business_clients': [{'id':i.id, 'name':i.name} for i in self.line_of_business_clients]
        }

class Sector(db.Model):
    __tablename__ = 'sectors'
    __table_args__ = (
        db.ForeignKeyConstraint(['line_of_business_id'], ['line_of_business.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    line_of_business_id = db.Column(db.Integer, nullable=False) # FK
    sector_line_of_business = db.relationship('LineOfBusiness', back_populates='line_of_business_sectors') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'line_of_business_id': self.line_of_business_id,
            'line_of_business': self.sector_line_of_business.name
        }

class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id']),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    is_approved = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_archived = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    juristiction = db.Column(db.Enum(Juristiction), nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    project_client = db.relationship('Client', back_populates='client_projects') # FK

    project_sectors = db.relationship('Sector', secondary=project_sector_link)
    project_users = db.relationship('Project', secondary=user_project_link)
    project_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_project', lazy='dynamic')
    project_transactions = db.relationship('Transaction', back_populates='transaction_project', lazy='dynamic')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

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
            'juristiction_code': self.juristiction.name,
            'juristiction_name': self.juristiction.value,
            'project_sectors': [i.serialize for i in self.project_sectors],
            'project_users': [{'id':i.id,'username':i.username} for i in self.project_users],
            'transaction_count': self.project_transactions.count()
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

class ParedownRule(db.Model):
    # these rules are only either core, or for a line_of_business
    # there are no project specific rules
    __tablename__ = 'paredown_rules'
    __table_args__ = (
        db.ForeignKeyConstraint(['line_of_business_id'], ['line_of_business.id'], ondelete='SET NULL'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    line_of_business_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    paredown_rule_line_of_business = db.relationship('LineOfBusiness', back_populates='line_of_business_paredown_rules') # FK
    #TODO add in rule saving data

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    vendor_transactions = db.relationship('Transaction', back_populates='transaction_vendor')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

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
            'vendor_transactions': [i.serialize for i in self.vendor_transactions]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

class DataMapping(db.Model):
    __tablename__ = 'data_mappings'
    __table_args__ = (
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['cdm_label_script_label'], ['cdm_labels.script_label']),
    )
    column_name = db.Column(db.String(256), nullable=False)
    table_name = db.Column(db.String(256), nullable=False)

    project_id = db.Column(db.Integer, nullable=False, primary_key=True) # FK
    data_mapping_project = db.relationship('Project', back_populates='project_data_mappings') # FK

    cdm_label_script_label = db.Column(db.String(256), nullable=False, primary_key=True) # FK
    data_mapping_cdm_label = db.relationship('CDM_label', back_populates='cdm_label_data_mappings') # FK

class CDM_label(db.Model):
    __tablename__ = 'cdm_labels'
    script_label = db.Column(db.String(256), primary_key=True, nullable=False)
    english_label = db.Column(db.String(256), nullable=False)
    is_calculated = db.Column(db.Boolean, unique=False, nullable=False)
    is_required = db.Column(db.Boolean, unique=False, nullable=False)
    is_unique = db.Column(db.Boolean, unique=False, nullable=False)
    datatype = db.Column(db.Enum(Datatype), nullable=False)
    regex = db.Column(db.String(256), nullable=False)

    cdm_label_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_cdm_label', lazy='dynamic')

################################################################################
# Prediction Models

# class ClassificationRule(db.Model):
#     __tablename__ = 'classification_rules'
#     __table_args__ = (
#         db.ForeignKeyConstraint(['line_of_business_id'], ['line_of_business.id'], ondelete='SET NULL'),
#         db.ForeignKeyConstraint(['client_id'], ['clients.id']),
#     )
#
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
#     weight = db.Column(db.Integer, nullable=False)
#
#     line_of_business_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
#     classification_rule_line_of_business = db.relationship('LineOfBusiness', back_populates='line_of_business_classification_rules') # FK
#
#     client_id = db.Column(db.Integer, nullable=False) # FK
#     classification_rule_client = db.relationship('Client', back_populates='client_classification_rules') # FK
    #TODO add in rule saving data

class ClientModel(db.Model):
    __tablename__ = 'client_models'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id']),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    status = db.Column(db.Enum(Activity), unique=False, server_default=Activity.pending.value, nullable=False)
    train_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    train_data_end = db.Column(db.DateTime(timezone=True), nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    client_model_client = db.relationship('Client', back_populates='client_client_models') # FK

    client_model_transactions = db.relationship('Transaction', back_populates='transaction_client_model', lazy='dynamic')
    client_model_model_performances = db.relationship('ClientModelPerformance', back_populates='performance_client_model', lazy='dynamic')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'created':self.created.strftime("%Y-%m-%d_%H:%M:%S"),
            'hyper_p': self.hyper_p,
            'status': self.status.value,
            'train_data_start': self.train_data_start.strftime('%Y/%m/%d'),
            'train_data_end': self.train_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_active_for_client(cls, id):
        return cls.query.filter_by(status = Activity.active.value).filter_by(id = id).first()

    @classmethod
    def set_active_for_client(cls, id):
        active_model = cls.find_active_for_client(id)
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=id).first().status = Activity.active.value
        db.session.commit()

class ClientModelPerformance(db.Model):
    __tablename__ = 'client_model_performances'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    precision = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    test_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    test_data_end =  db.Column(db.DateTime(timezone=True), nullable=False)

    client_model_id = db.Column(db.Integer, nullable=False) # FK
    performance_client_model = db.relationship('ClientModel', back_populates='client_model_model_performances') # FK

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class MasterModel(db.Model):
    __tablename__ = 'master_models'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    status = db.Column(db.Enum(Activity), unique=False, server_default=Activity.pending.value, nullable=False)
    train_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    train_data_end = db.Column(db.DateTime(timezone=True), nullable=False)

    master_model_transactions = db.relationship('Transaction', back_populates='transaction_master_model', lazy='dynamic')
    master_model_model_performances = db.relationship('MasterModelPerformance', back_populates='performance_master_model', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'created':self.created.strftime("%Y-%m-%d_%H:%M:%S"),
            'hyper_p': self.hyper_p,
            'status': self.status.value,
            'train_data_start': self.train_data_start.strftime('%Y/%m/%d'),
            'train_data_end': self.train_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def find_active(cls):
        return cls.query.filter_by(status = Activity.active.value).first()

    @classmethod
    def set_active(cls, id):
        active_model = cls.find_active()
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=id).first().status = Activity.active.value
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class MasterModelPerformance(db.Model):
    __tablename__ = 'master_model_performances'
    __table_args__ = (
        db.ForeignKeyConstraint(['master_model_id'], ['master_models.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    precision = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    test_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    test_data_end =  db.Column(db.DateTime(timezone=True), nullable=False)

    master_model_id = db.Column(db.Integer, nullable=False) # FK
    performance_master_model = db.relationship('MasterModel', back_populates='master_model_model_performances') # FK

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

################################################################################
class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = (
        db.ForeignKeyConstraint(['locked_user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['vendor_id'], ['vendors.id']),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['master_model_id'], ['master_models.id'], ondelete='SET NULL'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    modified = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_approved = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    rbc_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    rbc_recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    image = db.Column(db.LargeBinary, server_default=None, nullable=True)
    data = db.Column(postgresql.JSON, nullable=False)

    locked_user_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    locked_transaction_user = db.relationship('User', back_populates='locked_transactions') # FK

    vendor_id = db.Column(db.Integer, nullable=False) # FK
    transaction_vendor = db.relationship('Vendor', back_populates='vendor_transactions') # FK

    project_id = db.Column(db.Integer, nullable=False) # FK
    transaction_project = db.relationship('Project', back_populates='project_transactions') # FK

    client_model_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    transaction_client_model = db.relationship('ClientModel', back_populates='client_model_transactions') # FK

    master_model_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    transaction_master_model = db.relationship('MasterModel', back_populates='master_model_transactions') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'modified': self.modified.strftime("%Y-%m-%d_%H:%M:%S") if self.modified else None,
            'is_approved': self.is_approved,
            'is_predicted': self.is_predicted,
            'recovery_probability': self.recovery_probability,
            'rbc_predicted': self.rbc_predicted,
            'rbc_recovery_probability': self.rbc_recovery_probability,
            'data': self.data,
            'project_id': self.project_id,
            'locked_user_id': self.locked_user_id,
            'locked_user_initials': self.locked_transaction_user.initials,
            'client_model_id': self.client_model_id,
            'master_model_id': self.master_model_id
        }


##
