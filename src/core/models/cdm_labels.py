from src.core.models import db
from src.itra.models import Category, Caps_Interface, Datatype
################################################################################
class CDMLabel(db.Model):
    __tablename__ = 'cdm_labels'
    # data mapping
    script_label = db.Column(db.String(256), primary_key=True, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True, server_default='t')
    display_name = db.Column(db.String(256), nullable=True, default='', server_default='')

    # data dictionary
    is_calculated = db.Column(db.Boolean, unique=False, nullable=False, default=False, server_default='f')
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
