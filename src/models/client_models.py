from .__model_imports import *
from sqlalchemy import desc
################################################################################
class ClientModel(db.Model):
    __tablename__ = 'client_models'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id']),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    pickle = db.Column(db.PickleType, nullable=False)
    hyper_p = db.Column(postgresql.JSON, nullable=False)
    status = db.Column(db.Enum(Activity), unique=False, server_default=Activity.training.value, nullable=False)
    train_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    train_data_end = db.Column(db.DateTime(timezone=True), nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    client_model_client = db.relationship('Client', back_populates='client_client_models') # FK

    client_model_transactions = db.relationship('Transaction', back_populates='transaction_client_model', lazy='dynamic')
    client_model_model_performances = db.relationship('ClientModelPerformance', back_populates='performance_client_model', lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'created':self.created.strftime("%Y-%m-%d_%H:%M:%S"),
            'hyper_p': self.hyper_p,
            'name': "{}_{}_{}".format(self.client_model_client.name,self.created.strftime("%Y-%m-%d"),self.id),
            'status': self.status.value,
            'train_data_start': self.train_data_start.strftime('%Y/%m/%d'),
            'train_data_end': self.train_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_active_for_client(cls, client_id):
        return cls.query.filter_by(status = Activity.active.value).filter_by(client_id = client_id).first()

    @classmethod
    def find_pending_for_client(cls, client_id):
        return cls.query.filter_by(status = Activity.pending.value).filter_by(client_id = client_id).first()

    @classmethod
    def find_training_for_client(cls, client_id):
        return cls.query.filter_by(status = Activity.training.value).filter_by(client_id = client_id).first()

    @classmethod
    def set_active_for_client(cls, model_id, client_id):
        active_model = cls.find_active_for_client(client_id)
        if active_model:
            active_model.status = Activity.inactive.value
        cls.query.filter_by(id=model_id).first().status = Activity.active.value

class ClientModelPerformance(db.Model):
    __tablename__ = 'client_model_performances'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_model_id'], ['client_models.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    precision = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    test_data_start = db.Column(db.DateTime(timezone=True), nullable=False)
    test_data_end =  db.Column(db.DateTime(timezone=True), nullable=False)

    client_model_id = db.Column(db.Integer, nullable=False) # FK
    performance_client_model = db.relationship('ClientModel', back_populates='client_model_model_performances') # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_model_id': self.client_model_id,
            'created':self.created.strftime("%Y/%m/%d_%H:%M:%S"),
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'test_data_start': self.test_data_start.strftime('%Y/%m/%d'),
            'test_data_end': self.test_data_end.strftime('%Y/%m/%d')
        }

    @classmethod
    def get_most_recent_for_model(cls, model_id):
        return cls.query.filter_by(client_model_id=model_id).order_by(desc('created')).first()
