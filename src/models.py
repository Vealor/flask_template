import enum
import re
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import TypeDecorator, cast
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.types import Boolean, Date, DateTime, VARCHAR, Float, Integer, BLOB, DATE

db = SQLAlchemy()

################################################################################
# CUSTOM TYPES

class ArrayOfEnum(TypeDecorator):
    impl = postgresql.ARRAY
    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)
    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)
        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)
            return inner.split(",") if inner else []
        def process(value):
            if value is None:
                return None
            return [ i.serialize for i in super_rp(handle_raw_string(value))]
        return process

################################################################################
# ENUMS

class Roles(enum.Enum):
    tax_practitioner = "tax_practitioner"
    tax_approver = "tax_approver"
    tax_master = "tax_master"
    data_master = "data_master"
    administrative_assistant = "administrative_assistant"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class LineOfBusinessSectors(enum.Enum):
    business_services_business_services = {'lob':'Business Services','sec':'Business Services'}
    consumer_retail_consumer_goods = {'lob':'Consumer & Retail','sec':'Consumer Goods'}
    consumer_retail_food_beverage = {'lob':'Consumer & Retail','sec':'Food & Beverage'}
    consumer_retail_retail = {'lob':'Consumer & Retail','sec':'Retail'}
    energy_natural_resources_forestry = {'lob':'Energy & Natural Resources','sec':'Forestry'}
    energy_natural_resources_mining = {'lob':'Energy & Natural Resources','sec':'Mining'}
    energy_natural_resources_oil_gas_upstream = {'lob':'Energy & Natural Resources','sec':'Oil & Gas - Upstream'}
    energy_natural_resources_oil_gas_midstream = {'lob':'Energy & Natural Resources','sec':'Oil & Gas - Midstream'}
    energy_natural_resources_oil_gas_downstream = {'lob':'Energy & Natural Resources','sec':'Oil & Gas - Downstream'}
    energy_natural_resources_power_utilities = {'lob':'Energy & Natural Resources','sec':'Power & Utilities'}
    financial_services_asset_management = {'lob':'Financial Services','sec':'Asset Management'}
    financial_services_banking = {'lob':'Financial Services','sec':'Banking'}
    financial_services_insurance = {'lob':'Financial Services','sec':'Insurance'}
    financial_services_pensions = {'lob':'Financial Services','sec':'Pensions'}
    financial_services_private_equity = {'lob':'Financial Services','sec':'Private Equity'}
    financial_services_automotive = {'lob':'Industrial Markets','sec':'Automotive'}
    financial_services_chemicals = {'lob':'Industrial Markets','sec':'Chemicals'}
    financial_services_industrial_mfg = {'lob':'Industrial Markets','sec':'Industrial Mfg'}
    infrastructure_government_healthcare_aerospace_defense = {'lob':'Infrastructure, Government & Healthcare','sec':'Aerospace & Defense'}
    infrastructure_government_healthcare_government_services = {'lob':'Infrastructure, Government & Healthcare','sec':'Government Services'}
    infrastructure_government_healthcare_health_life_science = {'lob':'Infrastructure, Government & Healthcare','sec':'Health & Life Science'}
    infrastructure_government_healthcare_transport_infrastructure= {'lob':'Infrastructure, Government & Healthcare','sec':'Transport & Infrastructure'}
    real_estate_building_construct= {'lob':'Real Estate','sec':'Building & Construct'}
    real_estate_devleopers = {'lob':'Real Estate','sec':'Developers'}
    real_estate_hotels_recreation = {'lob':'Real Estate','sec':'Hotels & Recreation'}
    real_estate_invest_operator = {'lob':'Real Estate','sec':'Investors & Operator'}
    technology_media_telecommunication_media = {'lob':'Technology, Media & Telecommunication','sec':'Media'}
    technology_media_telecommunication_technology = {'lob':'Technology, Media & Telecommunication','sec':'Technology'}
    technology_media_telecommunication_telecommunications = {'lob':'Technology, Media & Telecommunication','sec':'Telecommunications'}

    @property
    def serialize(self):
        return {
            'code': self.name,
            'lob': self.value['lob'],
            'sec': self.value['sec']
        }

    @classmethod
    def list(cls):
        return list(map(lambda c: {'code':c.name,'lob':c.value['lob'],'sec':c.value['sec']}, cls))

class Actions(enum.Enum):
    create = "create"
    delete = "delete"
    modify = "modify"
    approve = "approve"

class Activity(enum.Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class Caps_Interface(enum.Enum):
    repetition = "repetition"
    caps_advanced = "caps_advanced"
    caps_basic = "caps_basic"
    sales = "sales"

class Category(enum.Enum):
    accounting = "Accounting"
    materials = "Materials"
    other = "Other"
    payment_details = "Payment Details"
    tax = "Tax"
    purchases = "Purchases"
    project_details = "Project Details"

class Datatype(enum.Enum):
    dt_boolean = Boolean
    dt_date = Date
    dt_datetime = DateTime
    dt_varchar = VARCHAR
    dt_float = Float
    dt_int = Integer
    dt_blob = BLOB

class ErrorTypes(enum.Enum):
    temp = "temp"

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

class Operator(enum.Enum):
    equals = "="
    greater_than_equals = ">="
    less_than_equals = "<="
    greater_than = ">"
    less_than = "<"

class Process(enum.Enum):
    aps_to_caps = "APS to CAPS"
    generate_aps = "Generate AP Subledger"
    caps_calculations = "CAPS Calculation fields"


################################################################################
# AUTH User and Token models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    initials = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)
    is_system_administrator = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    req_pass_reset = db.Column(db.Boolean, unique=False, default=True, server_default='t', nullable=False)

    user_projects = db.relationship('UserProject', back_populates='user_project_user', lazy='dynamic', passive_deletes=True)
    user_logs = db.relationship('Log', back_populates='log_user', lazy='dynamic')
    user_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_user', lazy='dynamic')

    # user_gst_coded_by = db.relationship('Transaction', back_populates='gst_coded_by_user', lazy='dynamic')
    # user_gst_signed_off_by = db.relationship('Transaction', back_populates='gst_signed_off_by_user', lazy='dynamic')
    # user_qst_coded_by = db.relationship('Transaction', back_populates='qst_coded_by_user', lazy='dynamic')
    # user_qst_signed_off_by = db.relationship('Transaction', back_populates='qst_signed_off_by_user', lazy='dynamic')
    # user_pst_coded_by = db.relationship('Transaction', back_populates='pst_coded_by_user', lazy='dynamic')
    # user_pst_signed_off_by = db.relationship('Transaction', back_populates='pst_signed_off_by_user', lazy='dynamic')
    # user_apo_coded_by = db.relationship('Transaction', back_populates='apo_coded_by_user', lazy='dynamic')
    # user_apo_signed_off_by = db.relationship('Transaction', back_populates='apo_signed_off_by_user', lazy='dynamic')

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
            'is_system_administrator': self.is_system_administrator,
            'is_superuser': self.is_superuser,
            'user_project_ids': [i.project_id for i in self.user_projects]
        }

    @property
    def serialize_user_proj(self):
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
            'is_system_administrator': self.is_system_administrator,
            'is_superuser': self.is_superuser,
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
    is_favourite = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    user_id = db.Column(db.Integer, nullable=False) # FK
    user_project_user = db.relationship('User', back_populates='user_projects') # FK

    project_id = db.Column(db.Integer, nullable=False) # FK
    user_project_project = db.relationship('Project', back_populates='project_users') # FK

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
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # client_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_client', cascade="save-update", lazy='dynamic')
    client_projects = db.relationship('Project', back_populates='project_client', cascade="save-update", lazy='dynamic', passive_deletes=True)
    client_client_models = db.relationship('ClientModel', back_populates='client_model_client', cascade="save-update", lazy='dynamic', passive_deletes=True)
    client_client_entities = db.relationship('ClientEntity', back_populates='client_entity_client', cascade="save-update", lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        active_model = [m for m in self.client_client_models if m.status.value == Activity.active.value]
        pending_model = [m for m in self.client_client_models if m.status.value == Activity.pending.value]
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'client_entities': [i.serialize for i in self.client_client_entities],
            'client_projects': [{'id':i.id, 'name':i.name} for i in self.client_projects],
            'client_inactive_models': [m.serialize for m in self.client_client_models if m.status.value == Activity.inactive.value],
            'client_pending_model': pending_model[0].serialize if pending_model else None,
            'client_active_model': active_model[0].serialize if active_model else None
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class ClientEntity(db.Model):
    __tablename__ = 'client_entities'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        db.UniqueConstraint('client_id', 'company_code', name='client_company_code_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_code = db.Column(db.String(4), nullable=False)
    lob_sector = db.Column(db.Enum(LineOfBusinessSectors), nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    client_entity_client = db.relationship('Client', back_populates='client_client_entities') # FK

    client_entity_jurisdictions = db.relationship('ClientEntityJurisdiction', back_populates='jurisdiction_client_entity', cascade="save-update", lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client_entity_client.name,
            'company_code': self.company_code,
            'lob_sector': self.lob_sector.serialize,
            'jurisdictions': [i.serialize for i in self.client_entity_jurisdictions]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class ClientEntityJurisdiction(db.Model):
    __tablename__ = 'client_entity_jurisdictions'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_entity_id'], ['client_entities.id'], ondelete='CASCADE'),
        db.UniqueConstraint('client_entity_id', 'jurisdiction', name='client_entity_jurisdiction_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jurisdiction = db.Column(db.Enum(Jurisdiction), nullable=False)

    client_entity_id = db.Column(db.Integer, nullable=False) # FK
    jurisdiction_client_entity = db.relationship('ClientEntity', back_populates='client_entity_jurisdictions')

    @property
    def serialize(self):
        return {
            'code': self.jurisdiction.name,
            'name': self.jurisdiction.value
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
    is_completed = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    project_client = db.relationship('Client', back_populates='client_projects') # FK

    engagement_partner_id = db.Column(db.Integer, nullable=False) # FK
    engagement_partner_user = db.relationship('User', foreign_keys='Project.engagement_partner_id') # FK

    engagement_manager_id = db.Column(db.Integer, nullable=False) # FK
    engagement_manager_user = db.relationship('User', foreign_keys='Project.engagement_manager_id') # FK

    project_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_project', cascade="save-update", lazy='dynamic', passive_deletes=True)
    project_users = db.relationship('UserProject', back_populates='user_project_project', lazy='dynamic', passive_deletes=True)
    project_transactions = db.relationship('Transaction', back_populates='transaction_project', lazy='dynamic', passive_deletes=True)
    project_data_params = db.relationship('DataParam', back_populates='data_param_project', lazy='dynamic', passive_deletes=True)

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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'client_id': self.client_id,
            'project_client': self.project_client.serialize,
            'is_paredown_locked': self.is_paredown_locked,
            'is_completed': self.is_completed,
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
    __tablename__ = 'paredown_rules'
    __table_args__ = (
        db.ForeignKeyConstraint(['paredown_rule_approver1_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['paredown_rule_approver2_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
        db.CheckConstraint('paredown_rule_approver1_id != paredown_rule_approver2_id'),
        db.CheckConstraint('is_core or (not is_core and not (bool(paredown_rule_approver1_id) or bool(paredown_rule_approver2_id)))'),
        db.CheckConstraint('((is_core and not coalesce(array_length(lob_sectors, 1), 0) > 0) or (not is_core and coalesce(array_length(lob_sectors, 1), 0) > 0))'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    comment = db.Column(db.String(128), nullable=True)

    lob_sectors = db.Column(ArrayOfEnum(postgresql.ENUM(LineOfBusinessSectors)), nullable=True)

    code_id = db.Column(db.Integer, nullable=False) # FK
    paredown_rule_code = db.relationship('Code', back_populates='code_paredown_rules')
    paredown_rule_approver1_id = db.Column(db.Integer, nullable=True) # FK
    paredown_rule_approver1_user = db.relationship('User', foreign_keys='ParedownRule.paredown_rule_approver1_id') # FK
    paredown_rule_approver2_id = db.Column(db.Integer, nullable=True) # FK
    paredown_rule_approver2_user = db.relationship('User', foreign_keys='ParedownRule.paredown_rule_approver2_id') # FK

    paredown_rule_conditions = db.relationship('ParedownRuleCondition', back_populates='paredown_rule_condition_paredown_rule', lazy='dynamic', passive_deletes=True) # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'is_core': self.is_core,
            'is_active': self.is_active,
            'conditions': [i.serialize for i in self.paredown_rule_conditions],
            'lob_sectors': self.lob_sectors if self.lob_sectors else [],
            'code': self.paredown_rule_code.serialize,
            'comment': self.comment,
            'approver1_id': self.paredown_rule_approver1_id,
            'approver1_username': self.paredown_rule_approver1_user.username if self.paredown_rule_approver1_id else None,
            'approver2_id': self.paredown_rule_approver2_id,
            'approver2_username': self.paredown_rule_approver2_user.username if self.paredown_rule_approver2_id else None
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class ParedownRuleCondition(db.Model):
    __tablename__ = 'paredown_rules_conditions'
    __table_args__ = (
        db.ForeignKeyConstraint(['paredown_rule_id'], ['paredown_rules.id'], ondelete='CASCADE'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    field = db.Column(db.String(128), nullable=False)
    operator = db.Column(db.String(128), nullable=False)
    value = db.Column(db.String(128), nullable=False)

    paredown_rule_id = db.Column(db.Integer, nullable=False) # FK
    paredown_rule_condition_paredown_rule = db.relationship('ParedownRule', back_populates='paredown_rule_conditions') #FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'field': self.field,
            'paredown_rule_id': self.paredown_rule_id,
            'operator': self.operator,
            'value': self.value
        }


class CapsGen(db.Model):
    __tablename__ = 'caps_gen'
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_completed = db.Column(db.Boolean, unique=False, nullable=False, default=False, server_default='f')
    __table_args__ += (
        db.Index('caps_gen_unique_completed', is_completed, unique=True, postgresql_where=(is_completed==False)),
    )

    user_id = db.Column(db.Integer, nullable=True) #FK
    caps_gen_user = db.relationship('User', back_populates='user_caps_gen')

    project_id = db.Column(db.Integer, nullable=False) # FK
    caps_gen_project = db.relationship('Project', back_populates='project_caps_gen')

    caps_gen_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcaps = db.relationship('SapCaps', back_populates='sapcaps_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapaps = db.relationship('SapAps', back_populates='sapaps_caps_gen', lazy='dynamic', passive_deletes=True)

    caps_gen_sapaufk = db.relationship('SapAufk', back_populates='sapaufk_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapbkpf = db.relationship('SapBkpf', back_populates='sapbkpf_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapbsak = db.relationship('SapBsak', back_populates='sapbsak_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapbseg = db.relationship('SapBseg', back_populates='sapbseg_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcepct = db.relationship('SapCepct', back_populates='sapcepct_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcsks = db.relationship('SapCsks', back_populates='sapcsks_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcskt = db.relationship('SapCskt', back_populates='sapcskt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapekko = db.relationship('SapEkko', back_populates='sapekko_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapekpo = db.relationship('SapEkpo', back_populates='sapekpo_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapiflot = db.relationship('SapIflot', back_populates='sapiflot_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapiloa = db.relationship('SapIloa', back_populates='sapiloa_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saplfa1 = db.relationship('SapLfa1', back_populates='saplfa1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmakt = db.relationship('SapMakt', back_populates='sapmakt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmara = db.relationship('SapMara', back_populates='sapmara_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sappayr = db.relationship('SapPayr', back_populates='sappayr_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapproj = db.relationship('SapProj', back_populates='sapproj_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapprps = db.relationship('SapPrps', back_populates='sapprps_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapregup = db.relationship('SapRegup', back_populates='sapregup_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapskat = db.relationship('SapSkat', back_populates='sapskat_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt001 = db.relationship('SapT001', back_populates='sapt001_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt007s = db.relationship('SapT007s', back_populates='sapt007s_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapska1 = db.relationship('SapSka1', back_populates='sapska1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapskb1 = db.relationship('SapSkb1', back_populates='sapskb1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt003t = db.relationship('SapT003t', back_populates='sapt003t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptbslt = db.relationship('SapTbslt', back_populates='saptbslt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptgsbt = db.relationship('SapTgsbt', back_populates='saptgsbt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saplfas = db.relationship('SapLfas', back_populates='saplfas_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saplfm1 = db.relationship('SapLfm1', back_populates='saplfm1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptoa01 = db.relationship('SapToa01', back_populates='saptoa01_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt024e = db.relationship('SapT024e', back_populates='sapt024e_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmlan = db.relationship('SapMlan', back_populates='sapmlan_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmseg = db.relationship('SapMseg', back_populates='sapmseg_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt001l = db.relationship('SapT001l', back_populates='sapt001l_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt006a = db.relationship('SapT006a', back_populates='sapt006a_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt023t = db.relationship('SapT023t', back_populates='sapt023t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptskmt = db.relationship('SapTskmt', back_populates='saptskmt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt005s = db.relationship('SapT005s', back_populates='sapt005s_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt007a = db.relationship('SapT007a', back_populates='sapt007a_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapttxjt = db.relationship('SapTtxjt', back_populates='sapttxjt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt001w = db.relationship('SapT001w', back_populates='sapt001w_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt005t = db.relationship('SapT005t', back_populates='sapt005t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptinct = db.relationship('SapTinct', back_populates='saptinct_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_gst_registration = db.relationship('GstRegistration', back_populates='gst_registration_caps_gen', lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        def caps_data_serialize(caps_data):
            return [{ 'id': i.id, 'data': i.data } for i in caps_data]
        return {
            'id': self.id,
            'created': self.created,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'project_name': self.caps_gen_project.name,
            'gst_registration': [i.serialize for i in self.caps_gen_gst_registration],
            'data_mappings': [i.serialize for i in self.caps_gen_data_mappings],
            'caps_data': {
                'caps_gen_sapaufk': caps_data_serialize(self.caps_gen_sapaufk),
                'caps_gen_sapbkpf': caps_data_serialize(self.caps_gen_sapbkpf),
                'caps_gen_sapbsak': caps_data_serialize(self.caps_gen_sapbsak),
                'caps_gen_sapbseg': caps_data_serialize(self.caps_gen_sapbseg),
                'caps_gen_sapcepct': caps_data_serialize(self.caps_gen_sapcepct),
                'caps_gen_sapcsks': caps_data_serialize(self.caps_gen_sapcsks),
                'caps_gen_sapcskt': caps_data_serialize(self.caps_gen_sapcskt),
                'caps_gen_sapekko': caps_data_serialize(self.caps_gen_sapekko),
                'caps_gen_sapekpo': caps_data_serialize(self.caps_gen_sapekpo),
                'caps_gen_sapiflot': caps_data_serialize(self.caps_gen_sapiflot),
                'caps_gen_sapiloa': caps_data_serialize(self.caps_gen_sapiloa),
                'caps_gen_saplfa1': caps_data_serialize(self.caps_gen_saplfa1),
                'caps_gen_sapmakt': caps_data_serialize(self.caps_gen_sapmakt),
                'caps_gen_sapmara': caps_data_serialize(self.caps_gen_sapmara),
                'caps_gen_sappayr': caps_data_serialize(self.caps_gen_sappayr),
                'caps_gen_sapproj': caps_data_serialize(self.caps_gen_sapproj),
                'caps_gen_sapprps': caps_data_serialize(self.caps_gen_sapprps),
                'caps_gen_sapregup': caps_data_serialize(self.caps_gen_sapregup),
                'caps_gen_sapskat': caps_data_serialize(self.caps_gen_sapskat),
                'caps_gen_sapt001': caps_data_serialize(self.caps_gen_sapt001),
                'caps_gen_sapt007s': caps_data_serialize(self.caps_gen_sapt007s),
                'caps_gen_sapskb1': caps_data_serialize(self.caps_gen_sapskb1),
                'caps_gen_sapt003t': caps_data_serialize(self.caps_gen_sapt003t),
                'caps_gen_saptbslt': caps_data_serialize(self.caps_gen_saptbslt),
                'caps_gen_saptgsbt': caps_data_serialize(self.caps_gen_saptgsbt),
                'caps_gen_saplfas': caps_data_serialize(self.caps_gen_saplfas),
                'caps_gen_saplfm1': caps_data_serialize(self.caps_gen_saplfm1),
                'caps_gen_saptoa01': caps_data_serialize(self.caps_gen_saptoa01),
                'caps_gen_sapt024e': caps_data_serialize(self.caps_gen_sapt024e),
                'caps_gen_sapmlan': caps_data_serialize(self.caps_gen_sapmlan),
                'caps_gen_sapmseg': caps_data_serialize(self.caps_gen_sapmseg),
                'caps_gen_sapt001l': caps_data_serialize(self.caps_gen_sapt001l),
                'caps_gen_sapt006a': caps_data_serialize(self.caps_gen_sapt006a),
                'caps_gen_sapt023t': caps_data_serialize(self.caps_gen_sapt023t),
                'caps_gen_saptskmt': caps_data_serialize(self.caps_gen_saptskmt),
                'caps_gen_sapt005s': caps_data_serialize(self.caps_gen_sapt005s),
                'caps_gen_sapt007a': caps_data_serialize(self.caps_gen_sapt007a),
                'caps_gen_sapttxjt': caps_data_serialize(self.caps_gen_sapttxjt),
                'caps_gen_sapt001w': caps_data_serialize(self.caps_gen_sapt001w),
                'caps_gen_sapt005t': caps_data_serialize(self.caps_gen_sapt005t),
                'caps_gen_saptinct': caps_data_serialize(self.caps_gen_saptinct)
            }
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class DataParam(db.Model):
    _tablename_ = 'data_params'
    __table_args__ = (
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    process = db.Column(db.Enum(Process), nullable=False)
    param = db.Column(db.String, nullable=False)
    operator = db.Column(db.Enum(Operator), nullable=False)
    value = db.Column(postgresql.ARRAY(db.String), nullable=True)
    is_many = db.Column(db.Boolean, nullable=False)

    project_id = db.Column(db.Integer, nullable=False, unique=True) # FK
    data_param_project = db.relationship('Project', back_populates='project_data_params')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'process': self.process.value,
            'param': self.param,
            'operator': self.operator.value,
            'value': [float(x) if re.match('^\d+(?:\.\d+)?$', x) else x for x in self.value],
            'is_many': self.is_many,
            'project_id': self.project_id
        }

class DataMapping(db.Model):
    __tablename__ = 'data_mappings'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['cdm_label_script_label'], ['cdm_labels.script_label']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    column_name = db.Column(db.String(256), nullable=True, default='', server_default='')
    table_name = db.Column(db.String(256), nullable=True, default='', server_default='')

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    data_mapping_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_data_mappings') # FK)

    cdm_label_script_label = db.Column(db.String(256), nullable=False) # FK
    data_mapping_cdm_label = db.relationship('CDMLabel', back_populates='cdm_label_data_mappings') # FK

    __table_args__ += (
        db.Index('caps_gen_mapping_col_table_unique', caps_gen_id, column_name, table_name, unique=True, postgresql_where=(db.and_(column_name!='', table_name!=''))),
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'caps_gen_id': self.caps_gen_id,
            'label': self.cdm_label_script_label,
            'display_name': self.data_mapping_cdm_label.display_name if self.data_mapping_cdm_label.display_name else None,
            'table_column_name': [{'table_name': self.table_name, 'column_name': self.column_name}] if self.table_name and self.column_name else [],
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class CDMLabel(db.Model):
    __tablename__ = 'cdm_labels'
    # data mapping
    script_label = db.Column(db.String(256), primary_key=True, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True, server_default='t')
    display_name = db.Column(db.String(256), nullable=True, default='', server_default='')

    # data dictionary
    is_calculated = db.Column(db.Boolean, unique=False, nullable=False)
    is_unique = db.Column(db.Boolean, unique=False, nullable=False)
    datatype = db.Column(db.Enum(Datatype), nullable=False)
    length = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    precision = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    caps_interface = db.Column(db.Enum(Caps_Interface), nullable=True)
    category = db.Column(db.Enum(Category), nullable=False)

    cdm_label_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_cdm_label', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'script_label': self.script_label,
            'is_active': self.is_active,
            'display_name': self.display_name,

            'is_calculated': self.is_calculated,
            'is_unique': self.is_unique,
            'datatype': self.datatype.name,
            'length': self.length,
            'precision': self.precision,
            'caps_interface': self.caps_interface.value if self.caps_interface else None,
        }
    @property
    def paredown_columns_serialize(self):
        return {
            'script_label': self.script_label,
            'display_name': self.display_name,
            'caps_interface': self.caps_interface
        }

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
    client_model_model_performances = db.relationship('ClientModelPerformance', back_populates='performance_client_model', lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'created':self.created.strftime("%Y-%m-%d_%H:%M:%S"),
            'name': self.client_model_client.name + "_" + str(self.id) + "_" + self.created.strftime("%Y-%m-%d"),
            'hyper_p': self.hyper_p,
            'status': self.status.value,
            'train_data_start': self.train_data_start.strftime('%Y/%m/%d'),
            'train_data_end': self.train_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_active_for_client(cls, client_id):
        return cls.query.filter_by(status = Activity.active.value).filter_by(client_id = client_id).first()

    @classmethod
    def set_active_for_client(cls, model_id, client_id):
        active_model = cls.find_active_for_client(client_id)
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=model_id).first().status = Activity.active.value

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
    master_model_model_performances = db.relationship('MasterModelPerformance', back_populates='performance_master_model', lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'created':self.created.strftime("%Y-%m-%d_%H:%M:%S"),
            'name': "Master_Model_" + str(self.id) + "_" + self.created.strftime("%Y-%m-%d"),
            'hyper_p': self.hyper_p,
            'status': self.status.value,
            'train_data_start': self.train_data_start.strftime('%Y/%m/%d'),
            'train_data_end': self.train_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_active(cls):
        return cls.query.filter_by(status = Activity.active.value).first()

    @classmethod
    def set_active(cls, model_id):
        active_model = cls.find_active()
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=model_id).first().status = Activity.active.value

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

################################################################################
class Code(db.Model):
    __tablename__ = 'codes'
    __table_args__ = (
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2048), nullable=True)

    code_paredown_rules = db.relationship('ParedownRule', back_populates='paredown_rule_code', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code_number': self.code_number,
            'description': self.description
        }

class ErrorCategory(db.Model):
    __tablename__ = 'error_categories'
    __table_args__ = (
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(2048), nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description
        }


class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = (
        db.ForeignKeyConstraint(['locked_user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['master_model_id'], ['master_models.id'], ondelete='SET NULL'),

        db.ForeignKeyConstraint(['gst_hst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['gst_hst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['gst_hst_signed_off_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['qst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['qst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['qst_signed_off_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['pst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['pst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['pst_signed_off_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['apo_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['apo_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['apo_signed_off_by_id'], ['users.id']),
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

    gst_hst_code_id = db.Column(db.Integer, nullable=True) #FK
    gst_code = db.relationship('Code', foreign_keys='Transaction.gst_hst_code_id') #FK
    gst_hst_notes = db.Column(db.String(2048), nullable=True)
    gst_hst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    gst_hst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    gst_hst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    gst_coded_by_user = db.relationship('User', foreign_keys='Transaction.gst_hst_coded_by_id') # FK
    gst_hst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    gst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.gst_hst_signed_off_by_id') # FK

    qst_code_id = db.Column(db.Integer, nullable=True) #FK
    qst_code = db.relationship('Code', foreign_keys='Transaction.qst_code_id') #FK
    qst_notes = db.Column(db.String(2048), nullable=True)
    qst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    qst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    qst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    qst_coded_by_user = db.relationship('User', foreign_keys='Transaction.qst_coded_by_id') # FK
    qst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    qst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.qst_signed_off_by_id') # FK

    pst_code_id = db.Column(db.Integer, nullable=True) #FK
    pst_code = db.relationship('Code', foreign_keys='Transaction.pst_code_id') #FK
    pst_notes = db.Column(db.String(2048), nullable=True)
    pst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    pst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    pst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    pst_coded_by_user = db.relationship('User', foreign_keys='Transaction.pst_coded_by_id') # FK
    pst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    pst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.pst_signed_off_by_id') # FK

    apo_code_id = db.Column(db.Integer, nullable=True) #FK
    apo_code = db.relationship('Code', foreign_keys='Transaction.apo_code_id') #FK
    apo_notes = db.Column(db.String(2048), nullable=True)
    apo_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    apo_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    apo_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    apo_coded_by_user = db.relationship('User', foreign_keys='Transaction.apo_coded_by_id') # FK
    apo_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    apo_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.apo_signed_off_by_id') # FK

    locked_user_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    locked_transaction_user = db.relationship('User', foreign_keys='Transaction.locked_user_id') # FK

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
            'codes': self.codes,
            'project_id': self.project_id,
            'locked_user_id': self.locked_user_id,
            'locked_user_initials': self.locked_transaction_user.initials if self.locked_transaction_user else None,
            'client_model_id': self.client_model_id,
            'master_model_id': self.master_model_id
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()


    # def update_prediction(self,update_dict):
    #     if 'client_model_id' in update_dict.keys():
    #         self.client_model_id = update_dict['client_model_id']
    #         self.master_model_id = None
    #     elif 'master_model_id' in update_dict.keys():
    #         self.master_model_id = update_dict['master_model_id']
    #         self.client_model_id = None
    #     else:
    #         raise ValueError("To update transaction, 'master_model_id' or 'client_model_id' must be specified.")
    #     self.recovery_probability = float(update_dict['recovery_probability'])
    #     self.is_predicted = True

class FXRates(db.Model):
    _tablename_ = 'fx_rates'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, unique=True)
    usdtocad = db.Column(db.Float, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'usdtocad': self.usdtocad
        }

class GstRegistration(db.Model):
    _tablename__ = 'gst_registration'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vendor_country = db.Column(db.String(64), nullable=True)
    vendor_number = db.Column(db.String(16), nullable=True)
    vendor_city = db.Column(db.String(16), nullable=True)
    vendor_region = db.Column(db.String(16), nullable=True)
    # TODO: how to mark this column
    duplicate_flag = db.Column(db.String(4), nullable=True)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    gst_registration_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_gst_registration') # FK

    @property
    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.gst_registration_caps_gen.project_id
        }

class SapCaps(db.Model):
    _tablename__ = 'sap_caps'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    # TODO: John add columns here

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapcaps_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcaps') # FK

    @property
    def serialize(self):
        return {
            "id": self.id,
            "caps_gen_id": self.caps_gen_id
        }

class SapAps(db.Model):
    _tablename__ = 'sap_aps'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    # TODO: John add columns here

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapaps_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapaps') # FK

    @property
    def serialize(self):
        return {
            "id": self.id,
            "caps_gen_id": self.caps_gen_id
        }

class SapBseg(db.Model):
    _tablename__ = 'sap_bseg'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapbseg_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapbseg') # FK

class SapAufk(db.Model):
    _tablename__ = 'sap_aufk'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapaufk_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapaufk') # FK

class SapBkpf(db.Model):
    _tablename__ = 'sap_bkpf'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapbkpf_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapbkpf') # FK

class SapRegup(db.Model):
    _tablename__ = 'sap_regup'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapregup_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapregup') # FK

class SapCepct(db.Model):
    _tablename__ = 'sap_cepct'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapcepct_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcepct') # FK

class SapCskt(db.Model):
    _tablename__ = 'sap_cskt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapcskt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcskt') # FK

class SapEkpo(db.Model):
    _tablename__ = 'sap_ekpo'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapekpo_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapekpo') # FK

class SapPayr(db.Model):
    _tablename__ = 'sap_payr'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sappayr_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sappayr') # FK

class SapBsak(db.Model):
    _tablename__ = 'sap_bsak'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapbsak_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapbsak') # FK

class SapCsks(db.Model):
    _tablename__ = 'sap_csks'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapcsks_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcsks') # FK

class SapEkko(db.Model):
    _tablename__ = 'sap_ekko'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapekko_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapekko') # FK

class SapIflot(db.Model):
    _tablename__ = 'sap_iflot'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapiflot_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapiflot') # FK

class SapIloa(db.Model):
    _tablename__ = 'sap_iloa'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapiloa_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapiloa') # FK

class SapSkat(db.Model):
    _tablename__ = 'sap_skat'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    sapskat_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapskat') # FK

class SapLfa1(db.Model):
    _tablename__ = 'sap_lfa1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False) # FK
    saplfa1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saplfa1') # FK

class SapMakt(db.Model):
    _tablename__ = 'sap_makt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapmakt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmakt') # FK

class SapMara(db.Model):
    _tablename__ = 'sap_mara'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapmara_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmara') # FK

class SapProj(db.Model):
    _tablename__ = 'sap_proj'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapproj_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapproj') # FK

class SapPrps(db.Model):
    _tablename__ = 'sap_prps'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapprps_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapprps') # FK

class SapT001(db.Model):
    _tablename__ = 'sap_t001'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt001_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt001') # FK

class SapT007s(db.Model):
    _tablename__ = 'sap_t007s'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt007s_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt007s') # FK


class SapSka1(db.Model):
    _tablename__ = 'sap_ska1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False)
    sapska1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapska1')


class SapSkb1(db.Model):
    _tablename__ = 'sap_skb1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapskb1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapskb1') # FK

class SapT003t(db.Model):
    _tablename__ = 'sap_t003t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt003t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt003t') # FK

class SapTbslt(db.Model):
    _tablename__ = 'sap_tbslt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saptbslt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptbslt') # FK

class SapTgsbt(db.Model):
    _tablename__ = 'sap_tbslt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saptgsbt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptgsbt') # FK

class SapLfas(db.Model):
    _tablename__ = 'sap_lfas'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saplfas_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saplfas') # FK

class SapLfm1(db.Model):
    _tablename__ = 'sap_lfm1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saplfm1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saplfm1') # FK

class SapT024e(db.Model):
    _tablename__ = 'sap_t024e'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt024e_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt024e') # FK

class SapToa01(db.Model):
    _tablename__ = 'sap_toa01'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saptoa01_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptoa01') # FK

class SapMlan(db.Model):
    _tablename__ = 'sap_mlan'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapmlan_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmlan') # FK

class SapMseg(db.Model):
    _tablename__ = 'sap_mseg'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapmseg_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmseg') # FK

class SapT001l(db.Model):
    _tablename__ = 'sap_t001l'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt001l_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt001l') # FK

class SapT006a(db.Model):
    _tablename__ = 'sap_t006a'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt006a_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt006a') # FK

class SapT023t(db.Model):
    _tablename__ = 'sap_t023t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt023t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt023t') # FK

class SapTskmt(db.Model):
    _tablename__ = 'sap_tskmt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saptskmt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptskmt') # FK

class SapT005s(db.Model):
    _tablename__ = 'sap_t005s'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt005s_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt005s') # FK

class SapT007a(db.Model):
    _tablename__ = 'sap_t007a'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt007a_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt007a') # FK

class SapTtxjt(db.Model):
    _tablename__ = 'sap_ttxjt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapttxjt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapttxjt') # FK

class SapT001w(db.Model):
    _tablename__ = 'sap_t001w'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt001w_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt001w') # FK

class SapT005t(db.Model):
    _tablename__ = 'sap_t005t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    sapt005t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt005t') # FK

class SapTinct(db.Model):
    _tablename__ = 'sap_tinct'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer,  nullable=False) # FK
    saptinct_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptinct') # FK
