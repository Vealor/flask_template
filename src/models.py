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
    tax_practitioner = "tax_practitioner"
    tax_approver = "tax_approver"
    tax_master = "tax_master"
    data_master = "data_master"
    administrative_assistant = "administrative_assistant"

    @classmethod
    def list(cls):
        return list(map(lambda c: {'code':c.name,'name':c.value}, cls))

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
    locked_transactions = db.relationship('Transaction', back_populates='locked_transaction_user', lazy='dynamic')

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
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'client_entities': [i.serialize for i in self.client_client_entities],
            'client_projects': [{'id':i.id, 'name':i.name} for i in self.client_projects]
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

    project_users = db.relationship('UserProject', back_populates='user_project_project', lazy='dynamic', passive_deletes=True)
    project_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_project', lazy='dynamic', passive_deletes=True)
    project_transactions = db.relationship('Transaction', back_populates='transaction_project', lazy='dynamic', passive_deletes=True)

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
    # these rules are only either core, or for a lob_sector
    # there are no project specific rules
    __tablename__ = 'paredown_rules'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    is_core = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    paredown_rule_lob_sectors = db.relationship('ParedownRuleLineOfBusinessSector', back_populates='lob_sector_paredown_rule', cascade="save-update", lazy='dynamic')
    #TODO add in rule saving data

class ParedownRuleLineOfBusinessSector(db.Model):
    __tablename__ = 'paredown_rule_lob_sector'
    __table_args__ = (
        db.ForeignKeyConstraint(['paredown_rule_id'], ['paredown_rules.id'], ondelete='CASCADE'),
        db.UniqueConstraint('paredown_rule_id', 'lob_sector', name='paredown_rule_lob_sector_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    lob_sector = db.Column(db.Enum(LineOfBusinessSectors), nullable=False)

    paredown_rule_id = db.Column(db.Integer, nullable=False) # FK
    lob_sector_paredown_rule = db.relationship('ParedownRule', back_populates='paredown_rule_lob_sectors')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'lob_sector': self.lob_sector.serialize
        }

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)

    vendor_transactions = db.relationship('Transaction', back_populates='transaction_vendor')

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
    client_model_model_performances = db.relationship('ClientModelPerformance', back_populates='performance_client_model', lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
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


##
