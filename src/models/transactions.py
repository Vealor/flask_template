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

        # db.ForeignKeyConstraint(['gst_hst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['gst_hst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['gst_hst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['qst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['qst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['qst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['pst_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['pst_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['pst_signed_off_by_id'], ['users.id']),
        # db.ForeignKeyConstraint(['apo_code_id'], ['codes.id']),
        db.ForeignKeyConstraint(['apo_coded_by_id'], ['users.id']),
        db.ForeignKeyConstraint(['apo_signed_off_by_id'], ['users.id']),

        db.CheckConstraint('gst_hst_coded_by_id != gst_hst_signed_off_by_id'),
        db.CheckConstraint('qst_coded_by_id != qst_signed_off_by_id'),
        db.CheckConstraint('pst_coded_by_id != pst_signed_off_by_id'),
        db.CheckConstraint('apo_coded_by_id != apo_signed_off_by_id'),
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
    {
    # transaction_attributes
    # even_gst_ind
    # odd_imm
    # prov_ap_amt
    # pme_imm
    # gst_imm
    # gst_count
    # cn_flag_ind
    # cn_rep2_ind
    # prov_ap
    # even_gst_rate
    # even_hst13_rate
    # even_hst14_rate
    # even_hst15_rate
    # even_gst_bc_rate
    # even_gst_mb_rate
    # even_gst_sask_rate
    # even_gst_qst_rate
    # pme_mat
    # gst_mat
    # flag_cn
    # odd_ind
    # pme_general
    # prov_tax_ind
    # eff_rate
    # rate_ind
    # new_vend_name
    # net_value
    # top_inv_amt
    # amount_local_ccy
    # ap_ar_amt_doc_ccy
    # vardocamt
    # vartranamount
    # varlocamt
    # ap_amt
    # gst_hst
    # pst
    # pst_sa
    # qst
    # taxes_other
    # varapkey
    # doc_type_gl
    # inv_date
    # post_date_gl
    # fx_rate
    # fiscal_period_gl
    # trnx_code_gl
    # ccy
    # inv_num
    # main_asset_num
    # asset_sub_num
    # gl_doc_num
    # post_key_gl
    # gl_doc_status
    # co_code_gl
    # po_doc_num
    # func_area_gl
    # fiscal_year_gl
    # bus_area_dept_num_gl
    # control_area_gl
    # cost_ctr_num_gl
    # cx_num
    # vend_num
    # material_num_gl
    # tax_type_gl
    # po_tax_code_gl
    # gst_hst_qst_pst_local_ccy
    # profit_ctr_num
    # wbs_gl
    # item_descr_gl
    # reverse_doc_num
    # reverse_reason_gl
    # tax_jur_gl
    # sales_doc_num_gl
    # billing_doc_num
    # gst_hst_pst_qst_doc_ccy
    # vend_name
    # vend_city
    # vend_region
    # vend_tax_num_1
    # vend_tax_num_2
    # vend_tax_num_3
    # vend_tax_num_4
    # vend_tax_num_5
    # vend_tax_num_type
    # vend_reg_num
    # lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl
    # post_key_descr
    # co_name
    # proj_loc_proj
    # proj_type_proj
    # wbs_elem_descr_proj
    # wbs_elem_id_proj
    # wbs_cntrl_area_proj
    # wbs_bus_area_proj
    # jv_obj_type_proj
    # object_num_proj
    # proj_descr_proj
    # proj_defin_proj
    # proj_internal_proj
    # proj_tx_jur_proj
    # proj_mngr_name_proj
    # proj_mngr_num_proj
    # bus_area_proj
    # plant_proj
    # tx_jur_descr_tx
    # plant_name_plant
    # plant_tx_jur_plant
    # tx_name_tx
    # largest_debit_half_acct_num_gl
    # pymt_doc_num_pmt
    # payee_code_pmt
    # cx_num_pmt
    # co_code_pmt
    # incoterms1
    # incoterms2
    # cntry_name
    # ean_upc_num_mat
    # mat_orig_ctry_mat
    # ean_categ_mat
    # mat_tx_class_mat
    # mat_tx_class_descr_mat
    # mat_group_descr_mat
    # mat_descr_mat
    # mat_dept_ctry_mat
    # mat_tx_ind_mat
    # wbs_po
    # po_tx_code_po
    # plant_num
    # po_tx_jur
    # po_item_descr
    # stor_loc_desc_mat
    # stor_loc_mat
    # stor_plant_mat
    # mat_doc_num_mat
    # mat_plnt_mat
    # punch_grp_po
    # punch_org_po
    # handover_loc_po
    # vend_phone
    # vend_person
    # purch_org_descr_po
    }



    transaction_codes = db.relationship('TransactionCode', back_populates='transaction_code_transaction', cascade="save-update", lazy='dynamic', passive_deletes=True) #FK

    gst_hst_notes_internal = db.Column(db.String(2048), server_default=None, nullable=True)
    gst_hst_notes_external = db.Column(db.String(2048), server_default=None, nullable=True)
    gst_hst_recoveries = db.Column(db.Float, nullable=True, default=0.0)
    gst_hst_error_type = db.Column(db.Enum(ErrorTypes), server_default=None, nullable=True)
    gst_hst_coded_by_id = db.Column(db.Integer, server_default=None, nullable=True) #FK
    gst_hst_coded_by_user = db.relationship('User', foreign_keys='Transaction.gst_hst_coded_by_id') # FK
    gst_hst_signed_off_by_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    gst_hst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.gst_hst_signed_off_by_id') # FK

    qst_notes_internal = db.Column(db.String(2048), server_default=None, nullable=True)
    qst_notes_external = db.Column(db.String(2048), server_default=None, nullable=True)
    qst_recoveries = db.Column(db.Float, server_default=None, nullable=True, default=0.0)
    qst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    qst_coded_by_id = db.Column(db.Integer, server_default=None, nullable=True) #FK
    qst_coded_by_user = db.relationship('User', foreign_keys='Transaction.qst_coded_by_id') # FK
    qst_signed_off_by_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    qst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.qst_signed_off_by_id') # FK

    pst_notes_internal = db.Column(db.String(2048), server_default=None, nullable=True)
    pst_notes_external = db.Column(db.String(2048), server_default=None, nullable=True)
    pst_recoveries = db.Column(db.Float, server_default=None, nullable=True, default=0.0)
    pst_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    pst_coded_by_id = db.Column(db.Integer, server_default=None, nullable=True) #FK
    pst_coded_by_user = db.relationship('User', foreign_keys='Transaction.pst_coded_by_id') # FK
    pst_signed_off_by_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
    pst_signed_off_by_user = db.relationship('User', foreign_keys='Transaction.pst_signed_off_by_id') # FK

    apo_notes_internal = db.Column(db.String(2048), server_default=None, nullable=True)
    apo_notes_external = db.Column(db.String(2048), server_default=None, nullable=True)
    apo_recoveries = db.Column(db.Float, server_default=None, nullable=True, default=0.0)
    apo_error_type = db.Column(db.Enum(ErrorTypes), nullable=True)
    apo_coded_by_id = db.Column(db.Integer, server_default=None, nullable=True) #FK
    apo_coded_by_user = db.relationship('User', foreign_keys='Transaction.apo_coded_by_id') # FK
    apo_signed_off_by_id = db.Column(db.Integer, server_default=None, nullable=True) # FK
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
        output = {
            'id': self.id,
            'modified': self.modified.strftime("%Y-%m-%d_%H:%M:%S") if self.modified else None,
            'is_paredowned': self.is_paredowned,
            'is_predicted': self.is_predicted,
            'recovery_probability': self.recovery_probability,
            'has_recoverable': self.recovery_probability >= 0.5 if self.recovery_probability else None,
            'rbc_predicted': self.rbc_predicted,
            'rbc_recovery_probability': self.rbc_recovery_probability,
            # 'data': self.data if self.data else {},
            'project_id': self.project_id,
            'locked_user_id': self.locked_user_id,
            'locked_user_initials': self.locked_transaction_user.initials if self.locked_transaction_user else None,
            'approved_user_id': self.approved_user_id,
            'approved_user_initials': self.approved_transaction_user.initials if self.approved_transaction_user else None,

            'client_model_id': self.client_model_id,
            'master_model_id': self.master_model_id,

            'gst_hst_codes': [c.serialize['code'] for c in self.transaction_codes if c.tax_type.value == 'gst'] if self.transaction_codes else [],
            'gst_hst_notes_internal': self.gst_hst_notes_internal,
            'gst_hst_notes_external': self.gst_hst_notes_external,
            'gst_hst_recoveries': self.gst_hst_recoveries,
            'gst_hst_error_type': self.gst_hst_error_type.name if self.gst_hst_error_type else None,
            'gst_hst_coded_by_id': self.gst_hst_coded_by_id,
            'gst_hst_coded_by_user': self.gst_hst_coded_by_user.username if self.gst_hst_coded_by_user else None,
            'gst_hst_signed_off_by_id': self.gst_hst_signed_off_by_id,
            'gst_hst_signed_off_by_user': self.gst_hst_signed_off_by_user.username if self.gst_hst_signed_off_by_user else None,

            'qst_codes': [c.serialize['code'] for c in self.transaction_codes if c.tax_type.value == 'qst'] if self.transaction_codes else [],
            'qst_notes_internal': self.qst_notes_internal,
            'qst_notes_external': self.qst_notes_external,
            'qst_recoveries': self.qst_recoveries,
            'qst_error_type': self.qst_error_type.name if self.qst_error_type else None,
            'qst_coded_by_id': self.qst_coded_by_id,
            'qst_coded_by_user': self.qst_coded_by_user.username if self.qst_coded_by_user else None,
            'qst_signed_off_by_id': self.qst_signed_off_by_id,
            'qst_signed_off_by_user': self.qst_signed_off_by_user.username if self.qst_signed_off_by_user else None,

            'pst_codes': [c.serialize['code'] for c in self.transaction_codes if c.tax_type.value == 'pst'] if self.transaction_codes else [],
            'pst_notes_internal': self.pst_notes_internal,
            'pst_notes_external': self.pst_notes_external,
            'pst_recoveries': self.pst_recoveries,
            'pst_error_type': self.pst_error_type.name if self.pst_error_type else None,
            'pst_coded_by_id': self.pst_coded_by_id,
            'pst_coded_by_user': self.pst_coded_by_user.username if self.pst_coded_by_user else None,
            'pst_signed_off_by_id': self.pst_signed_off_by_id,
            'pst_signed_off_by_user': self.pst_signed_off_by_user.username if self.pst_signed_off_by_user else None,

            'apo_codes': [c.serialize['code'] for c in self.transaction_codes if c.tax_type.value == 'apo'] if self.transaction_codes else [],
            'apo_notes_internal': self.apo_notes_internal,
            'apo_notes_external': self.apo_notes_external,
            'apo_recoveries': self.apo_recoveries,
            'apo_error_type': self.apo_error_type.name if self.apo_error_type else None,
            'apo_coded_by_id': self.apo_coded_by_id,
            'apo_coded_by_user': self.apo_coded_by_user.username if self.apo_coded_by_user else None,
            'apo_signed_off_by_id': self.apo_signed_off_by_id,
            'apo_signed_off_by_user': self.apo_signed_off_by_user.username if self.apo_signed_off_by_user else None
        }
        return (self.id, output, self.data if self.data else {})

    @property
    def predictive_serialize(self):
        output = {
            'id': self.id,
            'data': self.data,
            'approved_user_id': self.approved_user_id,
            'codes': {}
        }
        if self.transaction_project.has_ts_gst_hst and self.gst_hst_signed_off_by_id:
            # output['codes']['gst_hst'] = [c.serialize['code'] for c in self.gst_hst_codes] if self.gst_hst_codes else []
            output['codes']['gst_hst'] = [c.transaction_code_code.code_number for c in self.transaction_codes if c.tax_type.value == 'gst_hst'] if self.transaction_codes else []
        if self.transaction_project.has_ts_qst and self.qst_signed_off_by_id:
            # output['codes']['qst'] = [c.serialize['code'] for c in self.qst_codes] if self.qst_codes else []
            output['codes']['qst'] = [c.transaction_code_code.code_number for c in self.transaction_codes if c.tax_type.value == 'qst'] if self.transaction_codes else []
        if self.transaction_project.has_ts_pst and self.pst_signed_off_by_id:
            # output['codes']['pst'] = [c.serialize['code'] for c in self.pst_codes] if self.pst_codes else []
            output['codes']['pst'] = [c.transaction_code_code.code_number for c in self.transaction_codes if c.tax_type.value == 'pst'] if self.transaction_codes else []
        if self.transaction_project.has_ts_apo and self.apo_signed_off_by_id:
            # output['codes']['apo'] = [c.serialize['code'] for c in self.apo_codes] if self.apo_codes else []
            output['codes']['apo'] = [c.transaction_code_code.code_number for c in self.transaction_codes if c.tax_type.value == 'apo'] if self.transaction_codes else []
        return output

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()


    def update_codes(self, input_codes, tax_type, tempsession=None):
        codes = list(set(input_codes))
        used_session = tempsession if tempsession else db.session
        query = used_session.query(TransactionCode).filter_by(transaction_id=self.id).filter_by(tax_type=eval("TaxTypes."+tax_type)).all()
        query_codes = ([txn.transaction_code_code.code_number for txn in query])
        codes.sort()
        query_codes.sort()
        if not codes == query_codes:
            for txn_codes in query:
                if txn_codes.transaction_code_code.code_number in codes:
                    codes.remove(txn_codes.transaction_code_code.code_number)
                else:
                    used_session.delete(txn_codes)
            for code in codes:
                code_query = used_session.query(Code).filter_by(code_number=code).first()
                if not code_query:
                    raise InputError("Code number {} does not exist.".format(code))
                used_session.add(TransactionCode(
                    transaction_id = self.id,
                    tax_type=eval("TaxTypes."+tax_type),
                    code_id = code_query.id
                ))
            return True
        else:
            return False
        used_session.flush()
