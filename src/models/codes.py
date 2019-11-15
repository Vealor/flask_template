from .__model_imports import *
################################################################################
class TransactionGSTCode(db.Model):
    __tablename__ = 'transaction_gst_codes'
    __table_args__ = (
        db.ForeignKeyConstraint(['transaction_id'], ['transactions.id']),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    transaction_id = db.Column(db.Integer, nullable=False) # FK
    transaction_gst_code_transaction = db.relationship('Transaction', back_populates='gst_codes') # FK

    code_id = db.Column(db.Integer, nullable=False) # FK
    transaction_gst_code_code = db.relationship('Code', back_populates='code_gst_transactions') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code': self.transaction_gst_code_code.code_number
        }
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class TransactionHSTCode(db.Model):
    __tablename__ = 'transaction_hst_codes'
    __table_args__ = (
        db.ForeignKeyConstraint(['transaction_id'], ['transactions.id']),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    transaction_id = db.Column(db.Integer, nullable=False) # FK
    transaction_hst_code_transaction = db.relationship('Transaction', back_populates='hst_codes') # FK

    code_id = db.Column(db.Integer, nullable=False) # FK
    transaction_hst_code_code = db.relationship('Code', back_populates='code_hst_transactions') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code': self.transaction_hst_code_code.code_number
        }
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class TransactionQSTCode(db.Model):
    __tablename__ = 'transaction_qst_codes'
    __table_args__ = (
        db.ForeignKeyConstraint(['transaction_id'], ['transactions.id']),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    transaction_id = db.Column(db.Integer, nullable=False) # FK
    transaction_qst_code_transaction = db.relationship('Transaction', back_populates='qst_codes') # FK

    code_id = db.Column(db.Integer, nullable=False) # FK
    transaction_qst_code_code = db.relationship('Code', back_populates='code_qst_transactions') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code': self.transaction_qst_code_code.code_number
        }
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class TransactionPSTCode(db.Model):
    __tablename__ = 'transaction_pst_codes'
    __table_args__ = (
        db.ForeignKeyConstraint(['transaction_id'], ['transactions.id']),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    transaction_id = db.Column(db.Integer, nullable=False) # FK
    transaction_pst_code_transaction = db.relationship('Transaction', back_populates='pst_codes') # FK

    code_id = db.Column(db.Integer, nullable=False) # FK
    transaction_pst_code_code = db.relationship('Code', back_populates='code_pst_transactions') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code': self.transaction_pst_code_code.code_number
        }
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class TransactionAPOCode(db.Model):
    __tablename__ = 'transaction_apo_codes'
    __table_args__ = (
        db.ForeignKeyConstraint(['transaction_id'], ['transactions.id']),
        db.ForeignKeyConstraint(['code_id'], ['codes.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    transaction_id = db.Column(db.Integer, nullable=False) # FK
    transaction_apo_code_transaction = db.relationship('Transaction', back_populates='apo_codes') # FK

    code_id = db.Column(db.Integer, nullable=False) # FK
    transaction_apo_code_code = db.relationship('Code', back_populates='code_apo_transactions') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code': self.transaction_apo_code_code.code_number
        }
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class Code(db.Model):
    __tablename__ = 'codes'
    __table_args__ = (
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2048), nullable=True)

    code_gst_transactions = db.relationship('TransactionGSTCode', back_populates='transaction_gst_code_code')
    code_hst_transactions = db.relationship('TransactionHSTCode', back_populates='transaction_hst_code_code')
    code_qst_transactions = db.relationship('TransactionQSTCode', back_populates='transaction_qst_code_code')
    code_pst_transactions = db.relationship('TransactionPSTCode', back_populates='transaction_pst_code_code')
    code_apo_transactions = db.relationship('TransactionAPOCode', back_populates='transaction_apo_code_code')

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
