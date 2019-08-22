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

    @classmethod
    def list(cls):
        return list(map(lambda c: {'code':c.name,'name':c.value}, cls))

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

class Jurisdiction(enum.Enum):
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

    @property
    def serialize(self):
        return {
            'code': self.name,
            'name': self.value
        }

    @classmethod
    def list(cls):
        return list(map(lambda c: {'code':c.name,'name':c.value}, cls))

################################################################################
# Many 2 Many links

project_sector_link = db.Table('project_sector',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    db.Column('sector_id', db.Integer, db.ForeignKey('sectors.id', ondelete='CASCADE'), nullable=False, primary_key=True)
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
    role = db.Column(db.Enum(Roles), nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    req_pass_reset = db.Column(db.Boolean, unique=False, default=True, server_default='t', nullable=False)

    user_projects = db.relationship('UserProject', back_populates='user_project_user', lazy='dynamic', passive_deletes=True)
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
            'role': self.role.name
        }

    @property
    def serialize_proj(self):
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

class UserProject(db.Model):
    __tablename__ = 'user_project'
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.UniqueConstraint('user_id', 'project_id', name='user_project_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_project_user = db.relationship('User', back_populates='user_projects')
    project_id = db.Column(db.Integer, nullable=False)
    user_project_project = db.relationship('Project', back_populates='project_users')
    is_favourite = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

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
            'user_id': self.user_id,
            'user': self.user_project_user.username,
            'project_id': self.project_id,
            'project': self.user_project_project.serialize,
            'is_favourite': self.is_favourite
        }

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
            'line_of_business_id': self.line_of_business_id,
            'client_line_of_business': self.client_line_of_business.name,
            'client_projects': [{'id':i.id, 'name':i.name} for i in self.client_projects]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id']),
        db.ForeignKeyConstraint(['engagement_partner_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['engagement_manager_id'], ['users.id'], ondelete='SET NULL'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    is_paredown_locked = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_archived = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    jurisdiction = db.Column(db.Enum(Jurisdiction), nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    project_client = db.relationship('Client', back_populates='client_projects') # FK

    engagement_partner_id = db.Column(db.Integer, nullable=False) # FK
    engagement_partner_user = db.relationship('User', foreign_keys='Project.engagement_partner_id') # FK

    engagement_manager_id = db.Column(db.Integer, nullable=False) # FK
    engagement_manager_user = db.relationship('User', foreign_keys='Project.engagement_manager_id') # FK

    project_sectors = db.relationship('Sector', secondary=project_sector_link)
    project_users = db.relationship('UserProject', back_populates='user_project_project', lazy='dynamic', passive_deletes=True)
    project_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_project', lazy='dynamic')
    project_transactions = db.relationship('Transaction', back_populates='transaction_project', lazy='dynamic')

    has_ts_gst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_hst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_qst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_pst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_vat = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_mft = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_ct = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_excise = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_customs = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_crown = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_freehold = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    has_es_caps = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_taxreturn = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_flowthrough = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_employeeexpense = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_pccards = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_coupons = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_creditnotes = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_edi = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_cars = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_duplpay = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_unapplcredit = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_missedearly = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_otheroverpay = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_firmanalysis = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_brokeranalysis = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_crowngca = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_crownalloc = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_crownincent = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lornri = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lorsliding = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lordeduct = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lorunder = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lormissed = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_gstreg = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_cvm = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_taxgl = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_aps = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_ars = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_fxrates = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_trt = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_daf = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def update_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        print('deleting')
        print(self)
        db.session.delete(self)
        print('deleted')
        db.session.flush()
        print('flushed')
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'client_id': self.client_id,
            'project_client': self.project_client.serialize,
            'is_paredown_locked': self.is_paredown_locked,
            'is_archived': self.is_archived,
            'area': 'TBD',
            'code': 'TBD',
            'jurisdiction': self.jurisdiction.serialize,
            'project_sectors': [i.serialize for i in self.project_sectors],
            'project_users': [{'user_id':i.user_id,'username':i.user_project_user.username} for i in self.project_users],
            'transaction_count': self.project_transactions.count(),
            'engagement_partner_id': self.engagement_partner_id,
            'engagement_manager_id': self.engagement_manager_id,
            'tax_scope': {
                'has_ts_gst': self.has_ts_gst,
                'has_ts_hst': self.has_ts_hst,
                'has_ts_qst': self.has_ts_qst,
                'has_ts_pst': self.has_ts_pst,
                'has_ts_vat': self.has_ts_vat,
                'has_ts_mft': self.has_ts_mft,
                'has_ts_ct': self.has_ts_ct,
                'has_ts_excise': self.has_ts_excise,
                'has_ts_customs': self.has_ts_customs,
                'has_ts_crown': self.has_ts_crown,
                'has_ts_freehold': self.has_ts_freehold
            },
            'engagement_scope': {
                'indirect_tax': {
                    'has_es_caps': self.has_es_caps,
                    'has_es_taxreturn': self.has_es_taxreturn,
                    'has_es_flowthrough': self.has_es_flowthrough,
                    'has_es_employeeexpense': self.has_es_employeeexpense,
                    'has_es_pccards': self.has_es_pccards,
                    'has_es_coupons': self.has_es_coupons,
                    'has_es_creditnotes': self.has_es_creditnotes,
                    'has_es_edi': self.has_es_edi,
                    'has_es_cars': self.has_es_cars
                },
                'accounts_payable': {
                    'has_es_duplpay': self.has_es_duplpay,
                    'has_es_unapplcredit': self.has_es_unapplcredit,
                    'has_es_missedearly': self.has_es_missedearly,
                    'has_es_otheroverpay': self.has_es_otheroverpay
                },
                'customs': {
                    'has_es_firmanalysis': self.has_es_firmanalysis,
                    'has_es_brokeranalysis': self.has_es_brokeranalysis
                },
                'royalties': {
                    'has_es_crowngca': self.has_es_crowngca,
                    'has_es_crownalloc': self.has_es_crownalloc,
                    'has_es_crownincent': self.has_es_crownincent,
                    'has_es_lornri': self.has_es_lornri,
                    'has_es_lorsliding': self.has_es_lorsliding,
                    'has_es_lordeduct': self.has_es_lordeduct,
                    'has_es_lorunder': self.has_es_lorunder,
                    'has_es_lormissed': self.has_es_lormissed
                },
                'data': {
                    'has_es_gstreg': self.has_es_gstreg,
                    'has_es_cvm': self.has_es_cvm,
                    'has_es_taxgl': self.has_es_taxgl,
                    'has_es_aps': self.has_es_aps,
                    'has_es_ars': self.has_es_ars,
                    'has_es_fxrates': self.has_es_fxrates,
                    'has_es_trt': self.has_es_trt,
                    'has_es_daf': self.has_es_daf
                }
            }
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

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
            'vendor_transactions': [i.id for i in self.vendor_transactions]
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
    def set_active_for_client(cls, model_id, client_id):
        active_model = cls.find_active_for_client( client_id)
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=model_id).first().status = Activity.active.value
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
    def set_active(cls, model_id):
        active_model = cls.find_active()
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=model_id).first().status = Activity.active.value
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
            'locked_user_initials': self.locked_transaction_user.initials if self.locked_transaction_user else None,
            'client_model_id': self.client_model_id,
            'master_model_id': self.master_model_id
        }


    def update_prediction(self,update_dict):
        if 'client_model_id' in update_dict.keys():
            self.client_model_id = update_dict['client_model_id']
            self.master_model_id = None
        elif 'master_model_id' in update_dict.keys():
            self.master_model_id = update_dict['master_model_id']
            self.client_model_id = None
        else:
            raise ValueError("To update transaction, 'master_model_id' or 'client_model_id' must be specified.")
        self.recovery_probability = float(update_dict['recovery_probability'])
        self.is_predicted = True
        self.update_to_db()


    def update_to_db(self):
        db.session.commit()


##
