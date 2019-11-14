from .__model_imports import *
################################################################################
class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = (
        db.ForeignKeyConstraint(['client_id'], ['clients.id']),
        db.ForeignKeyConstraint(['engagement_partner_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['engagement_manager_id'], ['users.id'], ondelete='SET NULL'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    is_paredown_locked = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    is_completed = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    client_id = db.Column(db.Integer, nullable=False) # FK
    project_client = db.relationship('Client', back_populates='client_projects') # FK

    engagement_partner_id = db.Column(db.Integer, nullable=False) # FK
    engagement_partner_user = db.relationship('User', foreign_keys='Project.engagement_partner_id') # FK

    engagement_manager_id = db.Column(db.Integer, nullable=False) # FK
    engagement_manager_user = db.relationship('User', foreign_keys='Project.engagement_manager_id') # FK

    project_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_project', cascade="save-update", lazy='dynamic', passive_deletes=True)
    project_users = db.relationship('UserProject', back_populates='user_project_project', lazy='dynamic', passive_deletes=True)
    project_transactions = db.relationship('Transaction', back_populates='transaction_project', lazy='dynamic', passive_deletes=True)
    project_data_params = db.relationship('DataParam', back_populates='data_param_project', lazy='dynamic', passive_deletes=True)

    has_ts_gst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_hst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_qst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_pst = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_apo = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_vat = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_mft = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_ct = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_excise = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_customs = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_crown = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_ts_freehold = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    has_es_caps = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_taxreturn = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_flowthrough = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_employeeexpense = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_pccards = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_coupons = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_creditnotes = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_edi = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_cars = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_duplpay = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_unapplcredit = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_missedearly = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_otheroverpay = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_firmanalysis = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_brokeranalysis = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_crowngca = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_crownalloc = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_crownincent = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lornri = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lorsliding = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lordeduct = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lorunder = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_lormissed = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_gstreg = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_cvm = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_taxgl = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_aps = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_ars = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_fxrates = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_trt = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)
    has_es_daf = db.Column(db.Boolean, unique=False, default=False, server_default='f', nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'client_id': self.client_id,
            'project_client': self.project_client.serialize,
            'is_paredown_locked': self.is_paredown_locked,
            'is_completed': self.is_completed,
            'project_users': [{'user_id':i.user_id,'username':i.user_project_user.username} for i in self.project_users],
            'transaction_count': self.project_transactions.count(),
            'engagement_partner_id': self.engagement_partner_id,
            'engagement_manager_id': self.engagement_manager_id,
            'tax_scope': {
                'has_ts_gst': self.has_ts_gst,
                'has_ts_hst': self.has_ts_hst,
                'has_ts_qst': self.has_ts_qst,
                'has_ts_pst': self.has_ts_pst,
                'has_ts_vat': self.has_ts_vat,
                'has_ts_mft': self.has_ts_mft,
                'has_ts_ct': self.has_ts_ct,
                'has_ts_excise': self.has_ts_excise,
                'has_ts_customs': self.has_ts_customs,
                'has_ts_crown': self.has_ts_crown,
                'has_ts_freehold': self.has_ts_freehold
            },
            'engagement_scope': {
                'indirect_tax': {
                    'has_es_caps': self.has_es_caps,
                    'has_es_taxreturn': self.has_es_taxreturn,
                    'has_es_flowthrough': self.has_es_flowthrough,
                    'has_es_employeeexpense': self.has_es_employeeexpense,
                    'has_es_pccards': self.has_es_pccards,
                    'has_es_coupons': self.has_es_coupons,
                    'has_es_creditnotes': self.has_es_creditnotes,
                    'has_es_edi': self.has_es_edi,
                    'has_es_cars': self.has_es_cars
                },
                'accounts_payable': {
                    'has_es_duplpay': self.has_es_duplpay,
                    'has_es_unapplcredit': self.has_es_unapplcredit,
                    'has_es_missedearly': self.has_es_missedearly,
                    'has_es_otheroverpay': self.has_es_otheroverpay
                },
                'customs': {
                    'has_es_firmanalysis': self.has_es_firmanalysis,
                    'has_es_brokeranalysis': self.has_es_brokeranalysis
                },
                'royalties': {
                    'has_es_crowngca': self.has_es_crowngca,
                    'has_es_crownalloc': self.has_es_crownalloc,
                    'has_es_crownincent': self.has_es_crownincent,
                    'has_es_lornri': self.has_es_lornri,
                    'has_es_lorsliding': self.has_es_lorsliding,
                    'has_es_lordeduct': self.has_es_lordeduct,
                    'has_es_lorunder': self.has_es_lorunder,
                    'has_es_lormissed': self.has_es_lormissed
                },
                'data': {
                    'has_es_gstreg': self.has_es_gstreg,
                    'has_es_cvm': self.has_es_cvm,
                    'has_es_taxgl': self.has_es_taxgl,
                    'has_es_aps': self.has_es_aps,
                    'has_es_ars': self.has_es_ars,
                    'has_es_fxrates': self.has_es_fxrates,
                    'has_es_trt': self.has_es_trt,
                    'has_es_daf': self.has_es_daf
                }
            }
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
