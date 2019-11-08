from .__model_imports import *
################################################################################
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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
