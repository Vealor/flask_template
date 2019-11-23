from .__model_imports import *
################################################################################
class FXRates(db.Model):
    __tablename__ = 'fx_rates'
    __table_args__ = (
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date, unique=True, nullable=False)
    usdtocad = db.Column(db.Float, nullable=False)

    @property
    def get_dates(self):
        return {
            'datetime': self.date,
        }

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date': str(self.date),
            'usdtocad': self.usdtocad
        }
