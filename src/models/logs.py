from . import db
from ._enums import Actions
from sqlalchemy.sql import func
################################################################################
class Log(db.Model):
    __tablename__ = 'logs'
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    action = db.Column(db.Enum(Actions), nullable=False)
    affected_entity = db.Column(db.String(256), nullable=False)
    details = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, nullable=False)  # FK
    log_user = db.relationship('User', back_populates='user_logs')  # FK

    @property
    def serialize(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d_%H:%M:%S"),
            'action': self.action.value,
            'affected_entity': self.affected_entity,
            'details': self.details,
            'user_id': self.user_id,
            'username': self.log_user.username
        }
