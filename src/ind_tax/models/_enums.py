import enum
from sqlalchemy.types import Boolean, Date, DateTime, VARCHAR, Float, Integer, BLOB

################################################################################
# ENUMS

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

class TaxTypes(enum.Enum):
    gst_hst = "gst_hst"
    qst = "qst"
    pst_bc = "pst_bc"
    pst_sk = "pst_sk"
    pst_mb = "pst_mb"
    apo = "apo"
