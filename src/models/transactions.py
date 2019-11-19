from .__model_imports import *
from .codes import *
from src.errors import *
################################################################################
class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = (
        db.ForeignKeyConstraint(['locked_user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['approved_user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['master_model_id'], ['master_models.id'], ondelete='SET NULL'),

        # db.ForeignKeyConstraint(['gst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['gst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['gst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['hst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['hst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['hst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['qst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['qst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['qst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['pst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['pst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['pst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['apo_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['apo_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['apo_signed_off_by_id'], ['users.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    modified = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_paredowned = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    rbc_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    rbc_recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    image = db.Column(db.LargeBinary, server_default=None, nullable=True)
    data = db.Column(postgresql.JSON, nullable=False)

    # gst_code_id = db.Column(db.Integer, nullable=True) #FK
    gst_codes = db.relationship('TransactionGSTCode', back_populates='transaction_gst_code_transaction', cascade="save-update", lazy='dynamic', uselist=True, passive_deletes=True) #FK
    gst_notes_internal = db.Column(db.String(2048), nullable=True)
    gst_notes_external = db.Column(db.String(2048), nullable=True)
    gst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    gst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    gst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    gst_coded_by_user = db.relationship('User', foreign_keys='Transaction.gst_coded_by_id') # FK
    gst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    gst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.gst_signed_off_by_id') # FK

    # hst_code_id = db.Column(db.Integer, nullable=True) #FK
    hst_codes = db.relationship('TransactionHSTCode', back_populates='transaction_hst_code_transaction', cascade="save-update", lazy='dynamic', uselist=True, passive_deletes=True) #FK
    hst_notes_internal = db.Column(db.String(2048), nullable=True)
    hst_notes_external = db.Column(db.String(2048), nullable=True)
    hst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    hst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    hst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    hst_coded_by_user = db.relationship('User', foreign_keys='Transaction.hst_coded_by_id') # FK
    hst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    hst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.hst_signed_off_by_id') # FK

    # qst_code_id = db.Column(db.Integer, nullable=True) #FK
    qst_codes = db.relationship('TransactionQSTCode', back_populates='transaction_qst_code_transaction', cascade="save-update", lazy='dynamic', uselist=True, passive_deletes=True) #FK
    qst_notes_internal = db.Column(db.String(2048), nullable=True)
    qst_notes_external = db.Column(db.String(2048), nullable=True)
    qst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    qst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    qst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    qst_coded_by_user = db.relationship('User', foreign_keys='Transaction.qst_coded_by_id') # FK
    qst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    qst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.qst_signed_off_by_id') # FK

    # pst_code_id = db.Column(db.Integer, nullable=True) #FK
    pst_codes = db.relationship('TransactionPSTCode', back_populates='transaction_pst_code_transaction', cascade="save-update", lazy='dynamic', uselist=True, passive_deletes=True) #FK
    pst_notes_internal = db.Column(db.String(2048), nullable=True)
    pst_notes_external = db.Column(db.String(2048), nullable=True)
    pst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    pst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    pst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    pst_coded_by_user = db.relationship('User', foreign_keys='Transaction.pst_coded_by_id') # FK
    pst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    pst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.pst_signed_off_by_id') # FK

    # apo_code_id = db.Column(db.Integer, nullable=True) #FK
    apo_codes = db.relationship('TransactionAPOCode', back_populates='transaction_apo_code_transaction', cascade="save-update", lazy='dynamic', uselist=True, passive_deletes=True) #FK
    apo_notes_internal = db.Column(db.String(2048), nullable=True)
    apo_notes_external = db.Column(db.String(2048), nullable=True)
    apo_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    apo_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    apo_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    apo_coded_by_user = db.relationship('User', foreign_keys='Transaction.apo_coded_by_id') # FK
    apo_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    apo_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.apo_signed_off_by_id') # FK

    locked_user_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    locked_transaction_user = db.relationship('User', foreign_keys='Transaction.locked_user_id') # FK

    approved_user_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    approved_transaction_user = db.relationship('User', foreign_keys='Transaction.approved_user_id') # FK

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
            'is_paredowned': self.is_paredowned,
            'is_predicted': self.is_predicted,
            'recovery_probability': self.recovery_probability,
            'rbc_predicted': self.rbc_predicted,
            'rbc_recovery_probability': self.rbc_recovery_probability,
            'data': self.data if self.data else {},
            'project_id': self.project_id,
            'locked_user_id': self.locked_user_id,
            'locked_user_initials': self.locked_transaction_user.initials if self.locked_transaction_user else None,
            'approved_user_id': self.approved_user_id,
            'approved_user_initials': self.approved_transaction_user.initials if self.approved_transaction_user else None,

            'client_model_id': self.client_model_id,
            'master_model_id': self.master_model_id,

            'gst_codes': [c.serialize['code'] for c in self.gst_codes] if self.gst_codes else [],
            'gst_notes_internal': self.gst_notes_internal,
            'gst_notes_external': self.gst_notes_external,
            'gst_recoveries': self.gst_recoveries,
            'gst_error_type': self.gst_error_type.name if self.gst_error_type else None,
            'gst_coded_by_id': self.gst_coded_by_id,
            'gst_coded_by_user': self.gst_coded_by_user.username if self.gst_coded_by_user else None,
            'gst_signed_off_by_id': self.gst_signed_off_by_id,
            'gst_signed_off_by_user': self.gst_signed_off_by_user.username if self.gst_signed_off_by_user else None,

            'hst_codes': [c.serialize['code'] for c in self.hst_codes] if self.hst_codes else [],
            'hst_notes_internal': self.hst_notes_internal,
            'hst_notes_external': self.hst_notes_external,
            'hst_recoveries': self.hst_recoveries,
            'hst_error_type': self.hst_error_type.name if self.hst_error_type else None,
            'hst_coded_by_id': self.hst_coded_by_id,
            'hst_coded_by_user': self.hst_coded_by_user.username if self.hst_coded_by_user else None,
            'hst_signed_off_by_id': self.hst_signed_off_by_id,
            'hst_signed_off_by_user': self.hst_signed_off_by_user.username if self.hst_signed_off_by_user else None,

            'qst_codes': [c.serialize['code'] for c in self.qst_codes] if self.qst_codes else [],
            'qst_notes_internal': self.qst_notes_internal,
            'qst_notes_external': self.qst_notes_external,
            'qst_recoveries': self.qst_recoveries,
            'qst_error_type': self.qst_error_type.name if self.qst_error_type else None,
            'qst_coded_by_id': self.qst_coded_by_id,
            'qst_coded_by_user': self.qst_coded_by_user.username if self.qst_coded_by_user else None,
            'qst_signed_off_by_id': self.qst_signed_off_by_id,
            'qst_signed_off_by_user': self.qst_signed_off_by_user.username if self.qst_signed_off_by_user else None,

            'pst_codes': [c.serialize['code'] for c in self.pst_codes] if self.pst_codes else [],
            'pst_notes_internal': self.pst_notes_internal,
            'pst_notes_external': self.pst_notes_external,
            'pst_recoveries': self.pst_recoveries,
            'pst_error_type': self.pst_error_type.name if self.pst_error_type else None,
            'pst_coded_by_id': self.pst_coded_by_id,
            'pst_coded_by_user': self.pst_coded_by_user.username if self.pst_coded_by_user else None,
            'pst_signed_off_by_id': self.pst_signed_off_by_id,
            'pst_signed_off_by_user': self.pst_signed_off_by_user.username if self.pst_signed_off_by_user else None,

            'apo_codes': [c.serialize['code'] for c in self.apo_codes] if self.apo_codes else [],
            'apo_notes_internal': self.apo_notes_internal,
            'apo_notes_external': self.apo_notes_external,
            'apo_recoveries': self.apo_recoveries,
            'apo_error_type': self.apo_error_type.name if self.apo_error_type else None,
            'apo_coded_by_id': self.apo_coded_by_id,
            'apo_coded_by_user': self.apo_coded_by_user.username if self.apo_coded_by_user else None,
            'apo_signed_off_by_id': self.apo_signed_off_by_id,
            'apo_signed_off_by_user': self.apo_signed_off_by_user.username if self.apo_signed_off_by_user else None
        }

    @property
    def predictive_serialize(self):
        output = {
            'id': self.id,
            'data': self.data,
            'approved_user_id': self.approved_user_id,
            'codes': {}
        }
        if self.transaction_project.has_ts_gst and self.gst_signed_off_by_id:
            output['codes']['gst'] = [c.serialize['code'] for c in self.gst_codes] if self.gst_codes else []
        if self.transaction_project.has_ts_hst and self.hst_signed_off_by_id:
            output['codes']['hst'] = [c.serialize['code'] for c in self.hst_codes] if self.hst_codes else []
        if self.transaction_project.has_ts_qst and self.qst_signed_off_by_id:
            output['codes']['qst'] = [c.serialize['code'] for c in self.qst_codes] if self.qst_codes else []
        if self.transaction_project.has_ts_pst and self.pst_signed_off_by_id:
            output['codes']['pst'] = [c.serialize['code'] for c in self.pst_codes] if self.pst_codes else []
        if self.transaction_project.has_ts_apo and self.apo_signed_off_by_id:
            output['codes']['apo'] = [c.serialize['code'] for c in self.apo_codes] if self.apo_codes else []
        return output

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()


    def update_gst_codes(self, codes):
        gst_codes = codes
        gst_query = TransactionGSTCode.query.filter_by(transaction_id=self.id).all()
        for gst in gst_query:
            if gst.transaction_gst_code_code.code_number in gst_codes:
                gst_codes.remove(gst.transaction_gst_code_code.code_number)
            else:
                db.session.delete(gst)
        for code in gst_codes:
            code_query = Code.query.filter_by(code_number=code).first()
            if not code_query:
                raise InputError("Code number {} does not exist.".format(code))
            db.session.add(TransactionGSTCode(
                transaction_id = self.id,
                code_id = code_query.id
            ))
        db.session.flush()

    def update_hst_codes(self, codes):
        hst_codes = codes
        hst_query = TransactionHSTCode.query.filter_by(transaction_id=self.id).all()
        for hst in hst_query:
            if hst.transaction_hst_code_code.code_number in hst_codes:
                hst_codes.remove(hst.transaction_hst_code_code.code_number)
            else:
                db.session.delete(hst)
        for code in hst_codes:
            code_query = Code.query.filter_by(code_number=code).first()
            if not code_query:
                raise InputError("Code number {} does not exist.".format(code))
            db.session.add(TransactionHSTCode(
                transaction_id = self.id,
                code_id = code_query.id
            ))
        db.session.flush()

    def update_qst_codes(self, codes):
        qst_codes = codes
        qst_query = TransactionQSTCode.query.filter_by(transaction_id=self.id).all()
        for qst in qst_query:
            if qst.transaction_qst_code_code.code_number in qst_codes:
                qst_codes.remove(qst.transaction_qst_code_code.code_number)
            else:
                db.session.delete(qst)
        for code in qst_codes:
            code_query = Code.query.filter_by(code_number=code).first()
            if not code_query:
                raise InputError("Code number {} does not exist.".format(code))
            db.session.add(TransactionQSTCode(
                transaction_id = self.id,
                code_id = code_query.id
            ))
        db.session.flush()

    def update_pst_codes(self, codes):
        pst_codes = codes
        pst_query = TransactionPSTCode.query.filter_by(transaction_id=self.id).all()
        for pst in pst_query:
            if pst.transaction_pst_code_code.code_number in pst_codes:
                pst_codes.remove(pst.transaction_pst_code_code.code_number)
            else:
                db.session.delete(pst)
        for code in pst_codes:
            code_query = Code.query.filter_by(code_number=code).first()
            if not code_query:
                raise InputError("Code number {} does not exist.".format(code))
            db.session.add(TransactionPSTCode(
                transaction_id = self.id,
                code_id = code_query.id
            ))
        db.session.flush()

    def update_apo_codes(self, codes):
        apo_codes = codes
        apo_query = TransactionAPOCode.query.filter_by(transaction_id=self.id).all()
        for apo in apo_query:
            if apo.transaction_apo_code_code.code_number in apo_codes:
                apo_codes.remove(apo.transaction_apo_code_code.code_number)
            else:
                db.session.delete(apo)
        for code in apo_codes:
            code_query = Code.query.filter_by(code_number=code).first()
            if not code_query:
                raise InputError("Code number {} does not exist.".format(code))
            db.session.add(TransactionAPOCode(
                transaction_id = self.id,
                code_id = code_query.id
            ))
        db.session.flush()
