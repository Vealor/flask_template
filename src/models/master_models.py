from .__model_imports import *
###############################################################################
class MasterModel(db.Model):
    __tablename__ = 'master_models'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    status = db.Column(db.Enum(Activity), unique=False, server_default=Activity.pending.value, nullable=False)
    train_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    train_data_end = db.Column(db.DateTime(timezone=True), nullable=False)

    master_model_transactions = db.relationship('Transaction', back_populates='transaction_master_model', lazy='dynamic')
    master_model_model_performances = db.relationship('MasterModelPerformance', back_populates='performance_master_model', lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'created':self.created.strftime("%Y-%m-%d_%H:%M:%S"),
            'hyper_p': self.hyper_p,
            'status': self.status.value,
            'train_data_start': self.train_data_start.strftime('%Y/%m/%d'),
            'train_data_end': self.train_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_active(cls):
        return cls.query.filter_by(status = Activity.active.value).first()

    @classmethod
    def set_active(cls, model_id):
        active_model = cls.find_active()
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=model_id).first().status = Activity.active.value

class MasterModelPerformance(db.Model):
    __tablename__ = 'master_model_performances'
    __table_args__ = (
        db.ForeignKeyConstraint(['master_model_id'], ['master_models.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    precision = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    test_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    test_data_end =  db.Column(db.DateTime(timezone=True), nullable=False)

    master_model_id = db.Column(db.Integer, nullable=False) # FK
    performance_master_model = db.relationship('MasterModel', back_populates='master_model_model_performances') # FK