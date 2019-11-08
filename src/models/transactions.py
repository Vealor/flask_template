from .__model_imports import *
################################################################################
class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = (
        db.ForeignKeyConstraint(['locked_user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['approved_user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['master_model_id'], ['master_models.id'], ondelete='SET NULL'),

        db.ForeignKeyConstraint(['gst_hst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['gst_hst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['gst_hst_signed_off_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['qst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['qst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['qst_signed_off_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['pst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['pst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['pst_signed_off_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['apo_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['apo_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['apo_signed_off_by_id'], ['users.id']),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    modified = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    rbc_predicted = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    rbc_recovery_probability = db.Column(db.Float, server_default=None, nullable=True)
    image = db.Column(db.LargeBinary, server_default=None, nullable=True)
    data = db.Column(postgresql.JSON, nullable=False)

    gst_hst_code_id = db.Column(db.Integer, nullable=True) #FK
    gst_code = db.relationship('Code', foreign_keys='Transaction.gst_hst_code_id') #FK
    gst_hst_notes = db.Column(db.String(2048), nullable=True)
    gst_hst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    gst_hst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    gst_hst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    gst_coded_by_user = db.relationship('User', foreign_keys='Transaction.gst_hst_coded_by_id') # FK
    gst_hst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    gst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.gst_hst_signed_off_by_id') # FK

    qst_code_id = db.Column(db.Integer, nullable=True) #FK
    qst_code = db.relationship('Code', foreign_keys='Transaction.qst_code_id') #FK
    qst_notes = db.Column(db.String(2048), nullable=True)
    qst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    qst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    qst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    qst_coded_by_user = db.relationship('User', foreign_keys='Transaction.qst_coded_by_id') # FK
    qst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    qst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.qst_signed_off_by_id') # FK

    pst_code_id = db.Column(db.Integer, nullable=True) #FK
    pst_code = db.relationship('Code', foreign_keys='Transaction.pst_code_id') #FK
    pst_notes = db.Column(db.String(2048), nullable=True)
    pst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    pst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    pst_coded_by_id = db.Column(db.Integer, nullable=True) #FK
    pst_coded_by_user = db.relationship('User', foreign_keys='Transaction.pst_coded_by_id') # FK
    pst_signed_off_by_id = db.Column(db.Integer, nullable=True) # FK
    pst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.pst_signed_off_by_id') # FK

    apo_code_id = db.Column(db.Integer, nullable=True) #FK
    apo_code = db.relationship('Code', foreign_keys='Transaction.apo_code_id') #FK
    apo_notes = db.Column(db.String(2048), nullable=True)
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
            'is_predicted': self.is_predicted,
            'recovery_probability': self.recovery_probability,
            'rbc_predicted': self.rbc_predicted,
            'rbc_recovery_probability': self.rbc_recovery_probability,
            'data': self.data,
            'project_id': self.project_id,
            'locked_user_id': self.locked_user_id,
            'locked_user_initials': self.locked_transaction_user.initials if self.locked_transaction_user else None,
            'approved_user_id': self.approved_user_id,
            'approved_user_initials': self.approved_transaction_user.initials if self.approved_transaction_user else None,
            'client_model_id': self.client_model_id,
            'master_model_id': self.master_model_id,

            'gst_hst_code_id': self.gst_hst_code_id,
            'gst_code': self.gst_code,
            'gst_hst_notes': self.gst_hst_notes,
            'gst_hst_recoveries': self.gst_hst_recoveries,
            'gst_hst_error_type': self.gst_hst_error_type,
            'gst_hst_coded_by_id': self.gst_hst_coded_by_id,
            'gst_coded_by_user': self.gst_coded_by_user,
            'gst_hst_signed_off_by_id': self.gst_hst_signed_off_by_id,
            'gst_signed_off_by_user': self.gst_signed_off_by_user,
            'qst_code_id': self.qst_code_id,
            'qst_code': self.qst_code,
            'qst_notes': self.qst_notes,
            'qst_recoveries': self.qst_recoveries,
            'qst_error_type': self.qst_error_type,
            'qst_coded_by_id': self.qst_coded_by_id,
            'qst_coded_by_user': self.qst_coded_by_user,
            'qst_signed_off_by_id': self.qst_signed_off_by_id,
            'qst_signed_off_by_user': self.qst_signed_off_by_user,
            'pst_code_id': self.pst_code_id,
            'pst_code': self.pst_code,
            'pst_notes': self.pst_notes,
            'pst_recoveries': self.pst_recoveries,
            'pst_error_type': self.pst_error_type,
            'pst_coded_by_id': self.pst_coded_by_id,
            'pst_coded_by_user': self.pst_coded_by_user,
            'pst_signed_off_by_id': self.pst_signed_off_by_id,
            'pst_signed_off_by_user': self.pst_signed_off_by_user,
            'apo_code_id': self.apo_code_id,
            'apo_code': self.apo_code,
            'apo_notes': self.apo_notes,
            'apo_recoveries': self.apo_recoveries,
            'apo_error_type': self.apo_error_type,
            'apo_coded_by_id': self.apo_coded_by_id,
            'apo_coded_by_user': self.apo_coded_by_user,
            'apo_signed_off_by_id': self.apo_signed_off_by_id,
            'apo_signed_off_by_user': self.apo_signed_off_by_user
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
