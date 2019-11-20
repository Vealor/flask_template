import enum
import re
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import TypeDecorator, cast
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.types import Boolean, Date, DateTime, VARCHAR, Float, Integer, BLOB, DATE
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
    modify = "modify"
    delete = "delete"
    approve = "approve"

class Activity(enum.Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"
    training = "training"

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
    example_error = "example_error"

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
    contains = 'contains'

class Process(enum.Enum):
    aps_to_caps = "APS to CAPS"
    generate_aps = "Generate AP Subledger"
    caps_calculations = "CAPS Calculation fields"
