from .__model_imports import db
################################################################################
class ErrorCategory(db.Model):
    __tablename__ = 'error_categories'
    __table_args__ = (
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(2048), nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description
        }
