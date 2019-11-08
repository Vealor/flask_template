from .__model_imports import *
################################################################################
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
