from .__model_imports import db
################################################################################
class GstRegistration(db.Model):
    __tablename__ = 'gst_registration'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vendor_country = db.Column(db.String(256), nullable=True)
    vendor_number = db.Column(db.String(256), nullable=True)
    vendor_city = db.Column(db.String(256), nullable=True)
    vendor_region = db.Column(db.String(256), nullable=True)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    gst_registration_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_gst_registration')  # FK

    @property
    def serialize(self):
        return {
            'vendor_country': self.vendor_country,
            'vendor_number': self.vendor_number,
            'vendor_city': self.vendor_city,
            'vendor_region': self.vendor_region,
            'project_id': self.gst_registration_caps_gen.project_id
        }
