from .__model_imports import *
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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
