from src.core.models import db
from src.ind_tax.models import TaxTypes
################################################################################
class Code(db.Model):
    __tablename__ = 'codes'
    __table_args__ = (

    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code_number = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(2048), nullable=True)

    code_transactions = db.relationship('TransactionCode', back_populates='transaction_code_code', lazy='dynamic')
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

class TransactionCode(db.Model):
    __tablename__ = 'transaction_codes'
    __table_args__ = (
        db.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['code_id'], ['codes.id'], ondelete='CASCADE'),
        db.UniqueConstraint('tax_type', 'transaction_id', 'code_id', name='transaction_code_unique_constraint')
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tax_type = db.Column(db.Enum(TaxTypes), unique=False, nullable=False)

    transaction_id = db.Column(db.Integer, nullable=False)  # FK
    transaction_code_transaction = db.relationship('Transaction', back_populates='transaction_codes')  # FK

    code_id = db.Column(db.Integer, nullable=False)  # FK
    transaction_code_code = db.relationship('Code', back_populates='code_transactions')  # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'tax_type': self.tax_type.value,
            'code': self.transaction_code_code.code_number
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
