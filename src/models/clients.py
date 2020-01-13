from .__model_imports import db, func, Activity, LineOfBusinessSectors, Jurisdiction
################################################################################
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # client_classification_rules = db.relationship('ClassificationRule', back_populates='classification_rule_client', cascade="save-update", lazy='dynamic')
    client_projects = db.relationship('Project', back_populates='project_client', cascade="save-update", lazy='dynamic', passive_deletes=True)
    client_client_models = db.relationship('ClientModel', back_populates='client_model_client', cascade="save-update", lazy='dynamic', passive_deletes=True)
    client_client_entities = db.relationship('ClientEntity', back_populates='client_entity_client', cascade="save-update", lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        active_model = [m for m in self.client_client_models if m.status.value == Activity.active.value]
        pending_model = [m for m in self.client_client_models if m.status.value == Activity.pending.value]
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created,
            'client_entities': [i.serialize for i in self.client_client_entities],
            'client_projects': [{'id': i.id, 'name': i.name} for i in self.client_projects],
            'client_inactive_models': [m.serialize for m in self.client_client_models if m.status.value == Activity.inactive.value],
            'client_pending_model': pending_model[0].serialize if pending_model else None,
            'client_active_model': active_model[0].serialize if active_model else None
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class ClientEntity(db.Model):
    __tablename__ = 'client_entities'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        db.UniqueConstraint('client_id', 'company_code', name='client_company_code_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_code = db.Column(db.String(4), nullable=False)
    lob_sector = db.Column(db.Enum(LineOfBusinessSectors), nullable=False)

    client_id = db.Column(db.Integer, nullable=False)  # FK
    client_entity_client = db.relationship('Client', back_populates='client_client_entities')  # FK

    client_entity_jurisdictions = db.relationship('ClientEntityJurisdiction', back_populates='jurisdiction_client_entity', cascade="save-update", lazy='dynamic', passive_deletes=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client_entity_client.name,
            'company_code': self.company_code,
            'lob_sector': self.lob_sector.serialize,
            'jurisdictions': [i.serialize for i in self.client_entity_jurisdictions]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

class ClientEntityJurisdiction(db.Model):
    __tablename__ = 'client_entity_jurisdictions'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_entity_id'], ['client_entities.id'], ondelete='CASCADE'),
        db.UniqueConstraint('client_entity_id', 'jurisdiction', name='client_entity_jurisdiction_unique_constraint'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jurisdiction = db.Column(db.Enum(Jurisdiction), nullable=False)

    client_entity_id = db.Column(db.Integer, nullable=False)  # FK
    jurisdiction_client_entity = db.relationship('ClientEntity', back_populates='client_entity_jurisdictions')

    @property
    def serialize(self):
        return {
            'code': self.jurisdiction.name,
            'name': self.jurisdiction.value
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
