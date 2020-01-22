from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from src.core.models import db
################################################################################
class CapsGen(db.Model):
    __tablename__ = 'caps_gen'
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        db.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_completed = db.Column(db.Boolean, unique=False, nullable=False, default=False, server_default='f')
    __table_args__ += (
        db.Index('caps_gen_unique_completed', is_completed, unique=True, postgresql_where=(is_completed == False)),  # noqa: E712
    )

    user_id = db.Column(db.Integer, nullable=True)  # FK
    caps_gen_user = db.relationship('User', back_populates='user_caps_gen')

    project_id = db.Column(db.Integer, nullable=False)  # FK
    caps_gen_project = db.relationship('Project', back_populates='project_caps_gen')

    caps_gen_data_mappings = db.relationship('DataMapping', back_populates='data_mapping_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcaps = db.relationship('SapCaps', back_populates='sapcaps_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapaps = db.relationship('SapAps', back_populates='sapaps_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sap_glnetcheck = db.relationship('SapGLNetCheck', back_populates='sap_glnetcheck_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sap_taxglextract = db.relationship('SapTaxGLExtract', back_populates='sap_taxglextract_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapaufk = db.relationship('SapAufk', back_populates='sapaufk_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapbkpf = db.relationship('SapBkpf', back_populates='sapbkpf_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapbsak = db.relationship('SapBsak', back_populates='sapbsak_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapbseg = db.relationship('SapBseg', back_populates='sapbseg_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcepc = db.relationship('SapCepc', back_populates='sapcepc_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcepct = db.relationship('SapCepct', back_populates='sapcepct_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcsks = db.relationship('SapCsks', back_populates='sapcsks_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapcskt = db.relationship('SapCskt', back_populates='sapcskt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapekko = db.relationship('SapEkko', back_populates='sapekko_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapekpo = db.relationship('SapEkpo', back_populates='sapekpo_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapiflot = db.relationship('SapIflot', back_populates='sapiflot_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapiloa = db.relationship('SapIloa', back_populates='sapiloa_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saplfa1 = db.relationship('SapLfa1', back_populates='saplfa1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmakt = db.relationship('SapMakt', back_populates='sapmakt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmara = db.relationship('SapMara', back_populates='sapmara_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sappayr = db.relationship('SapPayr', back_populates='sappayr_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapproj = db.relationship('SapProj', back_populates='sapproj_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapprps = db.relationship('SapPrps', back_populates='sapprps_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapregup = db.relationship('SapRegup', back_populates='sapregup_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt042zt = db.relationship('SapT042zt', back_populates='sapt042zt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapj_1atodct = db.relationship('SapJ_1atodct', back_populates='sapj_1atodct_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapskat = db.relationship('SapSkat', back_populates='sapskat_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt001 = db.relationship('SapT001', back_populates='sapt001_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt007s = db.relationship('SapT007s', back_populates='sapt007s_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapska1 = db.relationship('SapSka1', back_populates='sapska1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapskb1 = db.relationship('SapSkb1', back_populates='sapskb1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt003t = db.relationship('SapT003t', back_populates='sapt003t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptbslt = db.relationship('SapTbslt', back_populates='saptbslt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptcurt = db.relationship('SapTcurt', back_populates='saptcurt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptgsbt = db.relationship('SapTgsbt', back_populates='saptgsbt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saplfas = db.relationship('SapLfas', back_populates='saplfas_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saplfm1 = db.relationship('SapLfm1', back_populates='saplfm1_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptoa01 = db.relationship('SapToa01', back_populates='saptoa01_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt024 = db.relationship('SapT024', back_populates='sapt024_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt024e = db.relationship('SapT024e', back_populates='sapt024e_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmlan = db.relationship('SapMlan', back_populates='sapmlan_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapmseg = db.relationship('SapMseg', back_populates='sapmseg_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt001l = db.relationship('SapT001l', back_populates='sapt001l_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt006a = db.relationship('SapT006a', back_populates='sapt006a_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptmkm1t = db.relationship('SapTmkm1t', back_populates='saptmkm1t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptntpb = db.relationship('SapTntpb', back_populates='saptntpb_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt023t = db.relationship('SapT023t', back_populates='sapt023t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptskmt = db.relationship('SapTskmt', back_populates='saptskmt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptvegrt = db.relationship('SapTvegrt', back_populates='saptvegrt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptvtyt = db.relationship('SapTvtyt', back_populates='saptvtyt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt005s = db.relationship('SapT005s', back_populates='sapt005s_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt007a = db.relationship('SapT007a', back_populates='sapt007a_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapttxjt = db.relationship('SapTtxjt', back_populates='sapttxjt_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt001w = db.relationship('SapT001w', back_populates='sapt001w_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_sapt005t = db.relationship('SapT005t', back_populates='sapt005t_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_saptinct = db.relationship('SapTinct', back_populates='saptinct_caps_gen', lazy='dynamic', passive_deletes=True)
    caps_gen_gst_registration = db.relationship('GstRegistration', back_populates='gst_registration_caps_gen', lazy='dynamic', passive_deletes=True)

    table_list = [
        'caps_gen_sapaufk', 'caps_gen_sapbkpf', 'caps_gen_sapbsak',
        'caps_gen_sapbseg', 'caps_gen_sapcepc', 'caps_gen_sapcepct',
        'caps_gen_sapcsks', 'caps_gen_sapcskt', 'caps_gen_sapekko',
        'caps_gen_sapekpo', 'caps_gen_sapiflot', 'caps_gen_sapiloa',
        'caps_gen_saplfa1', 'caps_gen_sapmakt', 'caps_gen_sapmara',
        'caps_gen_sappayr', 'caps_gen_sapproj', 'caps_gen_sapprps',
        'caps_gen_sapregup', 'caps_gen_sapt042zt', 'caps_gen_sapj_1atodct',
        'caps_gen_sapskat', 'caps_gen_sapt001', 'caps_gen_sapt007s',
        'caps_gen_sapskb1', 'caps_gen_sapt003t', 'caps_gen_saptbslt',
        'caps_gen_saptcurt', 'caps_gen_saptgsbt', 'caps_gen_saplfas',
        'caps_gen_saplfm1', 'caps_gen_saptoa01', 'caps_gen_sapt024',
        'caps_gen_sapt024e', 'caps_gen_sapmlan', 'caps_gen_sapmseg',
        'caps_gen_sapt001l', 'caps_gen_sapt006a', 'caps_gen_saptmkm1t',
        'caps_gen_saptntpb', 'caps_gen_sapt023t', 'caps_gen_saptskmt',
        'caps_gen_saptvegrt', 'caps_gen_saptvtyt', 'caps_gen_sapt005s',
        'caps_gen_sapt007a', 'caps_gen_sapttxjt', 'caps_gen_sapt001w',
        'caps_gen_sapt005t', 'caps_gen_saptinct'
    ]

    @property
    def get_tables(self):
        return [i.partition('sap')[2].lower() for i in self.table_list]

    @property
    def get_headers(self):
        output = {}
        for table in self.table_list:
            output[table] = list(eval('self.' + table).first().data.keys()) if eval('self.' + table).first() else []
        return output

    @property
    def serialize(self):
        return {
            'id': self.id,
            'created': self.created,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'project_name': self.caps_gen_project.name
            # 'gst_registration': [i.serialize for i in self.caps_gen_gst_registration],
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

################################################################################
# SAP Tables
class SapCaps(db.Model):
    __tablename__ = 'sap_caps'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    transaction_attributes = db.Column(db.String(256), nullable=True)
    even_gst_ind = db.Column(db.String(256), nullable=True)
    odd_imm = db.Column(db.String(256), nullable=True)
    prov_ap_amt = db.Column(db.String(256), nullable=True)
    pme_imm = db.Column(db.String(256), nullable=True)
    gst_imm = db.Column(db.String(256), nullable=True)
    gst_count = db.Column(db.String(256), nullable=True)
    cn_flag_ind = db.Column(db.String(256), nullable=True)
    cn_rep2_ind = db.Column(db.String(256), nullable=True)
    prov_ap = db.Column(db.String(256), nullable=True)
    even_gst_rate = db.Column(db.String(256), nullable=True)
    even_hst13_rate = db.Column(db.String(256), nullable=True)
    even_hst14_rate = db.Column(db.String(256), nullable=True)
    even_hst15_rate = db.Column(db.String(256), nullable=True)
    even_gst_bc_rate = db.Column(db.String(256), nullable=True)
    even_gst_mb_rate = db.Column(db.String(256), nullable=True)
    even_gst_sask_rate = db.Column(db.String(256), nullable=True)
    even_gst_qst_rate = db.Column(db.String(256), nullable=True)
    pme_mat = db.Column(db.String(256), nullable=True)
    gst_mat = db.Column(db.String(256), nullable=True)
    flag_cn = db.Column(db.String(256), nullable=True)
    odd_ind = db.Column(db.String(256), nullable=True)
    pme_general = db.Column(db.String(256), nullable=True)
    prov_tax_ind = db.Column(db.String(256), nullable=True)
    eff_rate = db.Column(db.String(256), nullable=True)
    rate_ind = db.Column(db.String(256), nullable=True)
    new_vend_name = db.Column(db.String(256), nullable=True)
    net_value = db.Column(db.String(256), nullable=True)
    top_inv_amt = db.Column(db.String(256), nullable=True)
    amount_local_ccy = db.Column(db.String(256), nullable=True)
    ap_ar_amt_doc_ccy = db.Column(db.String(256), nullable=True)
    vardocamt = db.Column(db.String(256), nullable=True)
    vartranamount = db.Column(db.String(256), nullable=True)
    varlocamt = db.Column(db.String(256), nullable=True)
    ap_amt = db.Column(db.String(256), nullable=True)
    gst_hst = db.Column(db.String(256), nullable=True)
    pst = db.Column(db.String(256), nullable=True)
    pst_sa = db.Column(db.String(256), nullable=True)
    qst = db.Column(db.String(256), nullable=True)
    taxes_other = db.Column(db.String(256), nullable=True)
    varapkey = db.Column(db.String(256), nullable=True)
    doc_type_gl = db.Column(db.String(256), nullable=True)
    inv_date = db.Column(db.String(256), nullable=True)
    post_date_gl = db.Column(db.String(256), nullable=True)
    fx_rate = db.Column(db.String(256), nullable=True)
    fiscal_period_gl = db.Column(db.String(256), nullable=True)
    trnx_code_gl = db.Column(db.String(256), nullable=True)
    ccy = db.Column(db.String(256), nullable=True)
    inv_num = db.Column(db.String(256), nullable=True)
    main_asset_num = db.Column(db.String(256), nullable=True)
    asset_sub_num = db.Column(db.String(256), nullable=True)
    gl_doc_num = db.Column(db.String(256), nullable=True)
    post_key_gl = db.Column(db.String(256), nullable=True)
    gl_doc_status = db.Column(db.String(256), nullable=True)
    co_code_gl = db.Column(db.String(256), nullable=True)
    po_doc_num = db.Column(db.String(256), nullable=True)
    func_area_gl = db.Column(db.String(256), nullable=True)
    fiscal_year_gl = db.Column(db.String(256), nullable=True)
    bus_area_dept_num_gl = db.Column(db.String(256), nullable=True)
    control_area_gl = db.Column(db.String(256), nullable=True)
    cost_ctr_num_gl = db.Column(db.String(256), nullable=True)
    cx_num = db.Column(db.String(256), nullable=True)
    vend_num = db.Column(db.String(256), nullable=True)
    material_num_gl = db.Column(db.String(256), nullable=True)
    tax_type_gl = db.Column(db.String(256), nullable=True)
    po_tax_code_gl = db.Column(db.String(256), nullable=True)
    gst_hst_qst_pst_local_ccy = db.Column(db.String(256), nullable=True)
    profit_ctr_num = db.Column(db.String(256), nullable=True)
    profit_ctr_name = db.Column(db.String(256), nullable=True)
    profit_ctr_descr = db.Column(db.String(256), nullable=True)
    cost_ctr_name = db.Column(db.String(256), nullable=True)
    cost_ctr_descr = db.Column(db.String(256), nullable=True)
    wbs_gl = db.Column(db.String(256), nullable=True)
    item_descr_gl = db.Column(db.String(256), nullable=True)
    reverse_doc_num = db.Column(db.String(256), nullable=True)
    reverse_reason_gl = db.Column(db.String(256), nullable=True)
    tax_jur_gl = db.Column(db.String(256), nullable=True)
    sales_doc_num_gl = db.Column(db.String(256), nullable=True)
    billing_doc_num = db.Column(db.String(256), nullable=True)
    gst_hst_pst_qst_doc_ccy = db.Column(db.String(256), nullable=True)
    vend_name = db.Column(db.String(256), nullable=True)
    vend_city = db.Column(db.String(256), nullable=True)
    vend_region = db.Column(db.String(256), nullable=True)
    vend_cntry = db.Column(db.String(256), nullable=True)
    vend_tax_num_1 = db.Column(db.String(256), nullable=True)
    vend_tax_num_2 = db.Column(db.String(256), nullable=True)
    vend_tax_num_3 = db.Column(db.String(256), nullable=True)
    vend_tax_num_4 = db.Column(db.String(256), nullable=True)
    vend_tax_num_5 = db.Column(db.String(256), nullable=True)
    vend_tax_num_type = db.Column(db.String(256), nullable=True)
    vend_reg_num = db.Column(db.String(256), nullable=True)
    lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl = db.Column(db.String(256), nullable=True)
    post_key_descr = db.Column(db.String(256), nullable=True)
    co_name = db.Column(db.String(256), nullable=True)
    proj_loc_proj = db.Column(db.String(256), nullable=True)
    proj_type_proj = db.Column(db.String(256), nullable=True)
    wbs_elem_descr_proj = db.Column(db.String(256), nullable=True)
    wbs_elem_id_proj = db.Column(db.String(256), nullable=True)
    wbs_cntrl_area_proj = db.Column(db.String(256), nullable=True)
    wbs_bus_area_proj = db.Column(db.String(256), nullable=True)
    jv_obj_type_proj = db.Column(db.String(256), nullable=True)
    object_num_proj = db.Column(db.String(256), nullable=True)
    proj_descr_proj = db.Column(db.String(256), nullable=True)
    proj_defin_proj = db.Column(db.String(256), nullable=True)
    proj_internal_proj = db.Column(db.String(256), nullable=True)
    proj_tx_jur_proj = db.Column(db.String(256), nullable=True)
    proj_mngr_name_proj = db.Column(db.String(256), nullable=True)
    proj_mngr_num_proj = db.Column(db.String(256), nullable=True)
    bus_area_proj = db.Column(db.String(256), nullable=True)
    plant_proj = db.Column(db.String(256), nullable=True)
    tx_jur_descr_tx = db.Column(db.String(256), nullable=True)
    plant_name_plant = db.Column(db.String(256), nullable=True)
    plant_tx_jur_plant = db.Column(db.String(256), nullable=True)
    tx_name_tx = db.Column(db.String(256), nullable=True)
    largest_debit_half_acct_num_gl = db.Column(db.String(256), nullable=True)
    pymt_doc_num_pmt = db.Column(db.String(256), nullable=True)
    payee_code_pmt = db.Column(db.String(256), nullable=True)
    cx_num_pmt = db.Column(db.String(256), nullable=True)
    co_code_pmt = db.Column(db.String(256), nullable=True)
    incoterms1 = db.Column(db.String(256), nullable=True)
    incoterms2 = db.Column(db.String(256), nullable=True)
    cntry_name = db.Column(db.String(256), nullable=True)
    ean_upc_num_mat = db.Column(db.String(256), nullable=True)
    mat_orig_ctry_mat = db.Column(db.String(256), nullable=True)
    ean_categ_mat = db.Column(db.String(256), nullable=True)
    mat_tx_class_mat = db.Column(db.String(256), nullable=True)
    mat_tx_class_descr_mat = db.Column(db.String(256), nullable=True)
    mat_group_descr_mat = db.Column(db.String(256), nullable=True)
    mat_descr_mat = db.Column(db.String(256), nullable=True)
    mat_dept_ctry_mat = db.Column(db.String(256), nullable=True)
    mat_tx_ind_mat = db.Column(db.String(256), nullable=True)
    wbs_po = db.Column(db.String(256), nullable=True)
    po_tx_code_po = db.Column(db.String(256), nullable=True)
    plant_num = db.Column(db.String(256), nullable=True)
    po_tx_jur = db.Column(db.String(256), nullable=True)
    po_item_descr = db.Column(db.String(256), nullable=True)
    stor_loc_desc_mat = db.Column(db.String(256), nullable=True)
    stor_loc_mat = db.Column(db.String(256), nullable=True)
    stor_plant_mat = db.Column(db.String(256), nullable=True)
    mat_doc_num_mat = db.Column(db.String(256), nullable=True)
    mat_plnt_mat = db.Column(db.String(256), nullable=True)
    punch_grp_po = db.Column(db.String(256), nullable=True)
    punch_org_po = db.Column(db.String(256), nullable=True)
    handover_loc_po = db.Column(db.String(256), nullable=True)
    vend_phone = db.Column(db.String(256), nullable=True)
    vend_person = db.Column(db.String(256), nullable=True)
    purch_org_descr_po = db.Column(db.String(256), nullable=True)
    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapcaps_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcaps')  # FK

    @property
    def serialize(self):
        return {
            "id": self.id,
            "caps_gen_id": self.caps_gen_id,
            'transaction_attributes': self.transaction_attributes,
            'even_gst_ind': self.even_gst_ind,
            'odd_imm': self.odd_imm,
            'prov_ap_amt': self.prov_ap_amt,
            'pme_imm': self.pme_imm,
            'gst_imm': self.gst_imm,
            'gst_count': self.gst_count,
            'cn_flag_ind': self.cn_flag_ind,
            'cn_rep2_ind': self.cn_rep2_ind,
            'prov_ap': self.prov_ap,
            'even_gst_rate': self.even_gst_rate,
            'even_hst13_rate': self.even_hst13_rate,
            'even_hst14_rate': self.even_hst14_rate,
            'even_hst15_rate': self.even_hst15_rate,
            'even_gst_bc_rate': self.even_gst_bc_rate,
            'even_gst_mb_rate': self.even_gst_mb_rate,
            'even_gst_sask_rate': self.even_gst_sask_rate,
            'even_gst_qst_rate': self.even_gst_qst_rate,
            'pme_mat': self.pme_mat,
            'gst_mat': self.gst_mat,
            'flag_cn': self.flag_cn,
            'odd_ind': self.odd_ind,
            'pme_general': self.pme_general,
            'prov_tax_ind': self.prov_tax_ind,
            'eff_rate': self.eff_rate,
            'rate_ind': self.rate_ind,
            'new_vend_name': self.new_vend_name,
            'net_value': self.net_value,
            'top_inv_amt': self.top_inv_amt,
            'amount_local_ccy': self.amount_local_ccy,
            'ap_ar_amt_doc_ccy': self.ap_ar_amt_doc_ccy,
            'vardocamt': self.vardocamt,
            'vartranamount': self.vartranamount,
            'varlocamt': self.varlocamt,
            'ap_amt': self.ap_amt,
            'gst_hst': self.gst_hst,
            'pst': self.pst,
            'pst_sa': self.pst_sa,
            'qst': self.qst,
            'taxes_other': self.taxes_other,
            'varapkey': self.varapkey,
            'doc_type_gl': self.doc_type_gl,
            'inv_date': self.inv_date,
            'post_date_gl': self.post_date_gl,
            'fx_rate': self.fx_rate,
            'fiscal_period_gl': self.fiscal_period_gl,
            'trnx_code_gl': self.trnx_code_gl,
            'ccy': self.ccy,
            'inv_num': self.inv_num,
            'main_asset_num': self.main_asset_num,
            'asset_sub_num': self.asset_sub_num,
            'gl_doc_num': self.gl_doc_num,
            'post_key_gl': self.post_key_gl,
            'gl_doc_status': self.gl_doc_status,
            'co_code_gl': self.co_code_gl,
            'po_doc_num': self.po_doc_num,
            'func_area_gl': self.func_area_gl,
            'fiscal_year_gl': self.fiscal_year_gl,
            'bus_area_dept_num_gl': self.bus_area_dept_num_gl,
            'control_area_gl': self.control_area_gl,
            'cost_ctr_num_gl': self.cost_ctr_num_gl,
            'cx_num': self.cx_num,
            'vend_num': self.vend_num,
            'material_num_gl': self.material_num_gl,
            'tax_type_gl': self.tax_type_gl,
            'po_tax_code_gl': self.po_tax_code_gl,
            'gst_hst_qst_pst_local_ccy': self.gst_hst_qst_pst_local_ccy,
            'profit_ctr_num': self.profit_ctr_num,
            'wbs_gl': self.wbs_gl,
            'item_descr_gl': self.item_descr_gl,
            'reverse_doc_num': self.reverse_doc_num,
            'reverse_reason_gl': self.reverse_reason_gl,
            'tax_jur_gl': self.tax_jur_gl,
            'sales_doc_num_gl': self.sales_doc_num_gl,
            'billing_doc_num': self.billing_doc_num,
            'gst_hst_pst_qst_doc_ccy': self.gst_hst_pst_qst_doc_ccy,
            'vend_name': self.vend_name,
            'vend_city': self.vend_city,
            'vend_region': self.vend_region,
            'vend_tax_num_1': self.vend_tax_num_1,
            'vend_tax_num_2': self.vend_tax_num_2,
            'vend_tax_num_3': self.vend_tax_num_3,
            'vend_tax_num_4': self.vend_tax_num_4,
            'vend_tax_num_5': self.vend_tax_num_5,
            'vend_tax_num_type': self.vend_tax_num_type,
            'vend_reg_num': self.vend_reg_num,
            'lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl': self.lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl,
            'post_key_descr': self.post_key_descr,
            'co_name': self.co_name,
            'proj_loc_proj': self.proj_loc_proj,
            'proj_type_proj': self.proj_type_proj,
            'wbs_elem_descr_proj': self.wbs_elem_descr_proj,
            'wbs_elem_id_proj': self.wbs_elem_id_proj,
            'wbs_cntrl_area_proj': self.wbs_cntrl_area_proj,
            'wbs_bus_area_proj': self.wbs_bus_area_proj,
            'jv_obj_type_proj': self.jv_obj_type_proj,
            'object_num_proj': self.object_num_proj,
            'proj_descr_proj': self.proj_descr_proj,
            'proj_defin_proj': self.proj_defin_proj,
            'proj_internal_proj': self.proj_internal_proj,
            'proj_tx_jur_proj': self.proj_tx_jur_proj,
            'proj_mngr_name_proj': self.proj_mngr_name_proj,
            'proj_mngr_num_proj': self.proj_mngr_num_proj,
            'bus_area_proj': self.bus_area_proj,
            'plant_proj': self.plant_proj,
            'tx_jur_descr_tx': self.tx_jur_descr_tx,
            'plant_name_plant': self.plant_name_plant,
            'plant_tx_jur_plant': self.plant_tx_jur_plant,
            'tx_name_tx': self.tx_name_tx,
            'largest_debit_half_acct_num_gl': self.largest_debit_half_acct_num_gl,
            'pymt_doc_num_pmt': self.pymt_doc_num_pmt,
            'payee_code_pmt': self.payee_code_pmt,
            'cx_num_pmt': self.cx_num_pmt,
            'co_code_pmt': self.co_code_pmt,
            'incoterms1': self.incoterms1,
            'incoterms2': self.incoterms2,
            'cntry_name': self.cntry_name,
            'ean_upc_num_mat': self.ean_upc_num_mat,
            'mat_orig_ctry_mat': self.mat_orig_ctry_mat,
            'ean_categ_mat': self.ean_categ_mat,
            'mat_tx_class_mat': self.mat_tx_class_mat,
            'mat_tx_class_descr_mat': self.mat_tx_class_descr_mat,
            'mat_group_descr_mat': self.mat_group_descr_mat,
            'mat_descr_mat': self.mat_descr_mat,
            'mat_dept_ctry_mat': self.mat_dept_ctry_mat,
            'mat_tx_ind_mat': self.mat_tx_ind_mat,
            'wbs_po': self.wbs_po,
            'po_tx_code_po': self.po_tx_code_po,
            'plant_num': self.plant_num,
            'po_tx_jur': self.po_tx_jur,
            'po_item_descr': self.po_item_descr,
            'stor_loc_desc_mat': self.stor_loc_desc_mat,
            'stor_loc_mat': self.stor_loc_mat,
            'stor_plant_mat': self.stor_plant_mat,
            'mat_doc_num_mat': self.mat_doc_num_mat,
            'mat_plnt_mat': self.mat_plnt_mat,
            'punch_grp_po': self.punch_grp_po,
            'punch_org_po': self.punch_org_po,
            'handover_loc_po': self.handover_loc_po,
            'vend_phone': self.vend_phone,
            'vend_person': self.vend_person,
            'purch_org_descr_po': self.purch_org_descr_po
        }

class SapAps(db.Model):
    __tablename__ = 'sap_aps'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    varapkey = db.Column(db.String(256), nullable=False)
    vardocamt = db.Column(db.String(256), nullable=True)
    varlocamt = db.Column(db.String(256), nullable=True)
    bseg_shkzg_key = db.Column(db.String(256), nullable=True)
    bseg_pswbt_key = db.Column(db.String(256), nullable=True)
    bseg_dmbe2_key = db.Column(db.String(256), nullable=True)
    bseg_umskz_key = db.Column(db.String(256), nullable=True)
    bkpf_ktopl_key = db.Column(db.String(256), nullable=True)
    bkpf_belnr_key = db.Column(db.String(256), nullable=True)
    doc_type_gl = db.Column(db.String(256), nullable=True)
    inv_date = db.Column(db.String(256), nullable=True)
    post_date_gl = db.Column(db.String(256), nullable=True)
    bkpf_bukrs_key = db.Column(db.String(256), nullable=True)
    bkpf_gjahr_key = db.Column(db.String(256), nullable=True)
    fx_rate = db.Column(db.String(256), nullable=True)
    bkpf_kzwrs_key = db.Column(db.String(256), nullable=True)
    fiscal_period_gl = db.Column(db.String(256), nullable=True)
    trnx_code_gl = db.Column(db.String(256), nullable=True)
    ccy = db.Column(db.String(256), nullable=True)
    inv_num = db.Column(db.String(256), nullable=True)
    main_asset_num = db.Column(db.String(256), nullable=True)
    asset_sub_num = db.Column(db.String(256), nullable=True)
    gl_doc_num = db.Column(db.String(256), nullable=True)
    post_key_gl = db.Column(db.String(256), nullable=True)
    gl_doc_status = db.Column(db.String(256), nullable=True)
    bseg_budat_key = db.Column(db.String(256), nullable=True)
    co_code_gl = db.Column(db.String(256), nullable=True)
    bseg_buzei_key = db.Column(db.String(256), nullable=True)
    amount_local_ccy = db.Column(db.String(256), nullable=True)
    po_doc_num = db.Column(db.String(256), nullable=True)
    bseg_ebelp_key = db.Column(db.String(256), nullable=True)
    func_area_gl = db.Column(db.String(256), nullable=True)
    fiscal_year_gl = db.Column(db.String(256), nullable=True)
    bus_area_dept_num_gl = db.Column(db.String(256), nullable=True)
    largest_debit_half_acct_num_gl = db.Column(db.String(256), nullable=True)
    control_area_gl = db.Column(db.String(256), nullable=True)
    cost_ctr_num_gl = db.Column(db.String(256), nullable=True)
    cx_num = db.Column(db.String(256), nullable=True)
    vend_num = db.Column(db.String(256), nullable=True)
    material_num_gl = db.Column(db.String(256), nullable=True)
    tax_type_gl = db.Column(db.String(256), nullable=True)
    bseg_mwsk3_key = db.Column(db.String(256), nullable=True)
    po_tax_code_gl = db.Column(db.String(256), nullable=True)
    gst_hst_qst_pst_local_ccy = db.Column(db.String(256), nullable=True)
    bseg_pargb_key = db.Column(db.String(256), nullable=True)
    profit_ctr_num = db.Column(db.String(256), nullable=True)
    wbs_gl = db.Column(db.String(256), nullable=True)
    item_descr_gl = db.Column(db.String(256), nullable=True)
    reverse_doc_num = db.Column(db.String(256), nullable=True)
    reverse_reason_gl = db.Column(db.String(256), nullable=True)
    tax_jur_gl = db.Column(db.String(256), nullable=True)
    sales_doc_num_gl = db.Column(db.String(256), nullable=True)
    billing_doc_num = db.Column(db.String(256), nullable=True)
    gst_hst_pst_qst_doc_ccy = db.Column(db.String(256), nullable=True)
    ap_ar_amt_doc_ccy = db.Column(db.String(256), nullable=True)
    lfa1_land1_key = db.Column(db.String(256), nullable=True)
    lfa1_lifnr_key = db.Column(db.String(256), nullable=True)
    vend_name = db.Column(db.String(256), nullable=True)
    vend_city = db.Column(db.String(256), nullable=True)
    vend_region = db.Column(db.String(256), nullable=True)
    vend_tax_num_1 = db.Column(db.String(256), nullable=True)
    vend_tax_num_2 = db.Column(db.String(256), nullable=True)
    vend_tax_num_3 = db.Column(db.String(256), nullable=True)
    vend_tax_num_4 = db.Column(db.String(256), nullable=True)
    vend_tax_num_5 = db.Column(db.String(256), nullable=True)
    vend_tax_num_type = db.Column(db.String(256), nullable=True)
    vend_reg_num = db.Column(db.String(256), nullable=True)
    skat_ktopl_key = db.Column(db.String(256), nullable=True)
    skat_saknr_key = db.Column(db.String(256), nullable=True)
    skat_spras_key = db.Column(db.String(256), nullable=True)
    lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl = db.Column(db.String(256), nullable=True)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapaps_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapaps')  # FK

    @property
    def serialize(self):
        return {
            'inv_date': self.inv_date,
            'post_date_gl': self.post_date_gl,
            'fx_rate': self.fx_rate,
            'fiscal_period_gl': self.fiscal_period_gl,
            'trnx_code_gl': self.trnx_code_gl,
            'ccy': self.ccy,
            'inv_num': self.inv_num,
            'main_asset_num': self.main_asset_num,
            'asset_sub_num': self.asset_sub_num,
            'gl_doc_num': self.gl_doc_num,
            'gl_doc_status': self.gl_doc_status,
            'co_code_gl': self.co_code_gl,
            'amount_local_ccy': self.amount_local_ccy,
            'po_doc_num': self.po_doc_num,
            'func_area_gl': self.func_area_gl,
            'fiscal_year_gl': self.fiscal_year_gl,
            'bus_area_dept_num_gl': self.bus_area_dept_num_gl,
            'largest_debit_half_acct_num_gl': self.largest_debit_half_acct_num_gl,
            'control_area_gl': self.control_area_gl,
            'cost_ctr_num_gl': self.cost_ctr_num_gl,
            'cx_num': self.cx_num,
            'vend_num': self.vend_num,
            'material_num_gl': self.material_num_gl,
            'tax_type_gl': self.tax_type_gl,
            'po_tax_code_gl': self.po_tax_code_gl,
            'gst_hst_qst_pst_local_ccy': self.gst_hst_qst_pst_local_ccy,
            'profit_ctr_num': self.profit_ctr_num,
            'wbs_gl': self.wbs_gl,
            'item_descr_gl': self.item_descr_gl,
            'reverse_doc_num': self.reverse_doc_num,
            'reverse_reason_gl': self.reverse_reason_gl,
            'tax_jur_gl': self.tax_jur_gl,
            'sales_doc_num_gl': self.sales_doc_num_gl,
            'billing_doc_num': self.billing_doc_num,
            'gst_hst_pst_qst_doc_ccy': self.gst_hst_pst_qst_doc_ccy,
            'ap_ar_amt_doc_ccy': self.ap_ar_amt_doc_ccy,
            'lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl': self.lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl,
            'vend_name': self.vend_name,
            'vend_city': self.vend_city,
            'vend_region': self.vend_region,
            'vend_tax_num_1': self.vend_tax_num_1,
            'vend_tax_num_2': self.vend_tax_num_2,
            'vend_tax_num_3': self.vend_tax_num_3,
            'vend_tax_num_4': self.vend_tax_num_4,
            'vend_tax_num_5': self.vend_tax_num_5,
            'vend_tax_num_type': self.vend_tax_num_type,
            'vend_reg_num': self.vend_reg_num
        }


class SapTaxGLExtract(db.Model):
    __tablename__ = 'sap_taxglextract'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    co_code_gl = db.Column(db.String(256), nullable=True)
    gl_doc_num = db.Column(db.String(256), nullable=True)
    fiscal_year_gl = db.Column(db.String(256), nullable=True)
    bseg_buzei_key = db.Column(db.String(256), nullable=True)
    fiscal_period_gl = db.Column(db.String(256), nullable=True)
    doc_type_gl = db.Column(db.String(256), nullable=True)
    trnx_code_gl = db.Column(db.String(256), nullable=True)
    post_key_gl = db.Column(db.String(256), nullable=True)
    bseg_shkzg_key = db.Column(db.String(256), nullable=True)
    bus_area_dept_num_gl = db.Column(db.String(256), nullable=True)
    po_tax_code_gl = db.Column(db.String(256), nullable=True)
    item_descr_gl = db.Column(db.String(256), nullable=True)
    cost_ctr_num_gl = db.Column(db.String(256), nullable=True)
    largest_debit_half_acct_num_gl = db.Column(db.String(256), nullable=True)
    vend_num = db.Column(db.String(256), nullable=True)
    vend_name = db.Column(db.String(256), nullable=True)
    inv_num = db.Column(db.String(256), nullable=True)
    inv_date = db.Column(db.String(256), nullable=True)
    po_doc_num = db.Column(db.String(256), nullable=True)
    bseg_ebelp_key = db.Column(db.String(256), nullable=True)
    profit_ctr_num = db.Column(db.String(256), nullable=True)
    tax_jur_gl = db.Column(db.String(256), nullable=True)
    wbs_gl = db.Column(db.String(256), nullable=True)
    varapkey = db.Column(db.String(256), nullable=True)
    varlocamt = db.Column(db.String(256), nullable=True)
    vardocamt = db.Column(db.String(256), nullable=True)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sap_taxglextract_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sap_taxglextract')  # FK

    @property
    def serialize(self):
        return {
            'co_code_gl': self.co_code_gl,
            'gl_doc_num': self.gl_doc_num,
            'fiscal_year_gl': self.fiscal_year_gl,
            'bseg_buzei_key': self.bseg_buzei_key,
            'fiscal_period_gl': self.fiscal_period_gl,
            'doc_type_gl': self.doc_type_gl,
            'trnx_code_gl': self.trnx_code_gl,
            'post_key_gl': self.post_key_gl,
            'bseg_shkzg_key': self.bseg_shkzg_key,
            'bus_area_dept_num_gl': self.bus_area_dept_num_gl,
            'po_tax_code_gl': self.po_tax_code_gl,
            'item_descr_gl': self.item_descr_gl,
            'cost_ctr_num_gl': self.cost_ctr_num_gl,
            'largest_debit_half_acct_num_gl': self.largest_debit_half_acct_num_gl,
            'vend_num': self.vend_num,
            'vend_name': self.vend_name,
            'inv_num': self.inv_num,
            'inv_date': self.inv_date,
            'po_doc_num': self.po_doc_num,
            'bseg_ebelp_key': self.bseg_ebelp_key,
            'profit_ctr_num': self.profit_ctr_num,
            'tax_jur_gl': self.tax_jur_gl,
            'wbs_gl': self.wbs_gl,
            'varapkey': self.varapkey,
            'varlocamt': self.varlocamt,
            'vardocamt': self.vardocamt
        }


class SapGLNetCheck(db.Model):
    __tablename__ = 'sap_glnetcheck'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    varlocamt = db.Column(db.Float, nullable=True)
    vardocamt = db.Column(db.Float, nullable=True)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sap_glnetcheck_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sap_glnetcheck')  # FK

    @property
    def serialize(self):
        return {
            'varlocamt': self.varlocamt,
            'vardocamt': self.vardocamt
        }

class SapBseg(db.Model):
    __tablename__ = 'sap_bseg'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapbseg_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapbseg')  # FK

class SapAufk(db.Model):
    __tablename__ = 'sap_aufk'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapaufk_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapaufk')  # FK

class SapBkpf(db.Model):
    __tablename__ = 'sap_bkpf'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapbkpf_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapbkpf')  # FK

class SapRegup(db.Model):
    __tablename__ = 'sap_regup'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapregup_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapregup')  # FK

class SapT042zt(db.Model):
    __tablename__ = 'sap_t042zt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt042zt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt042zt')  # FK

class SapJ_1atodct(db.Model):
    __tablename__ = 'sap_j_1atodct'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapj_1atodct_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapj_1atodct')  # FK

class SapCepc(db.Model):
    __tablename__ = 'sap_cepc'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapcepc_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcepc')  # FK

class SapCepct(db.Model):
    __tablename__ = 'sap_cepct'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapcepct_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcepct')  # FK

class SapCskt(db.Model):
    __tablename__ = 'sap_cskt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapcskt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcskt')  # FK

class SapEkpo(db.Model):
    __tablename__ = 'sap_ekpo'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapekpo_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapekpo')  # FK

class SapPayr(db.Model):
    __tablename__ = 'sap_payr'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sappayr_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sappayr')  # FK

class SapBsak(db.Model):
    __tablename__ = 'sap_bsak'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapbsak_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapbsak')  # FK

class SapCsks(db.Model):
    __tablename__ = 'sap_csks'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapcsks_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapcsks')  # FK

class SapEkko(db.Model):
    __tablename__ = 'sap_ekko'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapekko_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapekko')  # FK

class SapIflot(db.Model):
    __tablename__ = 'sap_iflot'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapiflot_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapiflot')  # FK

class SapIloa(db.Model):
    __tablename__ = 'sap_iloa'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapiloa_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapiloa')  # FK

class SapSkat(db.Model):
    __tablename__ = 'sap_skat'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapskat_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapskat')  # FK

class SapLfa1(db.Model):
    __tablename__ = 'sap_lfa1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saplfa1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saplfa1')  # FK

class SapMakt(db.Model):
    __tablename__ = 'sap_makt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapmakt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmakt')  # FK

class SapMara(db.Model):
    __tablename__ = 'sap_mara'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapmara_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmara')  # FK

class SapProj(db.Model):
    __tablename__ = 'sap_proj'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapproj_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapproj')  # FK

class SapPrps(db.Model):
    __tablename__ = 'sap_prps'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapprps_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapprps')  # FK

class SapT001(db.Model):
    __tablename__ = 'sap_t001'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt001_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt001')  # FK

class SapT007s(db.Model):
    __tablename__ = 'sap_t007s'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt007s_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt007s')  # FK


class SapSka1(db.Model):
    __tablename__ = 'sap_ska1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)
    sapska1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapska1')


class SapSkb1(db.Model):
    __tablename__ = 'sap_skb1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapskb1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapskb1')  # FK

class SapT003t(db.Model):
    __tablename__ = 'sap_t003t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt003t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt003t')  # FK

class SapTbslt(db.Model):
    __tablename__ = 'sap_tbslt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptbslt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptbslt')  # FK

class SapTcurt(db.Model):
    __tablename__ = 'sap_tcurt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptcurt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptcurt')  # FK

class SapTgsbt(db.Model):
    __tablename__ = 'sap_tgsbt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptgsbt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptgsbt')  # FK

class SapLfas(db.Model):
    __tablename__ = 'sap_lfas'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saplfas_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saplfas')  # FK

class SapLfm1(db.Model):
    __tablename__ = 'sap_lfm1'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saplfm1_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saplfm1')  # FK

class SapT024(db.Model):
    __tablename__ = 'sap_t024'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt024_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt024')  # FK

class SapT024e(db.Model):
    __tablename__ = 'sap_t024e'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt024e_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt024e')  # FK

class SapToa01(db.Model):
    __tablename__ = 'sap_toa01'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptoa01_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptoa01')  # FK

class SapMlan(db.Model):
    __tablename__ = 'sap_mlan'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapmlan_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmlan')  # FK

class SapMseg(db.Model):
    __tablename__ = 'sap_mseg'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapmseg_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapmseg')  # FK

class SapT001l(db.Model):
    __tablename__ = 'sap_t001l'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt001l_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt001l')  # FK

class SapT006a(db.Model):
    __tablename__ = 'sap_t006a'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt006a_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt006a')  # FK

class SapTmkm1t(db.Model):
    __tablename__ = 'sap_tmkm1t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptmkm1t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptmkm1t')  # FK

class SapTntpb(db.Model):
    __tablename__ = 'sap_tntpb'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptntpb_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptntpb')  # FK

class SapT023t(db.Model):
    __tablename__ = 'sap_t023t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt023t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt023t')  # FK

class SapTskmt(db.Model):
    __tablename__ = 'sap_tskmt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptskmt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptskmt')  # FK

class SapTvegrt(db.Model):
    __tablename__ = 'sap_tvegrt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptvegrt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptvegrt')  # FK

class SapTvtyt(db.Model):
    __tablename__ = 'sap_tvtyt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptvtyt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptvtyt')  # FK

class SapT005s(db.Model):
    __tablename__ = 'sap_t005s'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt005s_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt005s')  # FK

class SapT007a(db.Model):
    __tablename__ = 'sap_t007a'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt007a_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt007a')  # FK

class SapTtxjt(db.Model):
    __tablename__ = 'sap_ttxjt'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapttxjt_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapttxjt')  # FK

class SapT001w(db.Model):
    __tablename__ = 'sap_t001w'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt001w_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt001w')  # FK

class SapT005t(db.Model):
    __tablename__ = 'sap_t005t'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    sapt005t_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_sapt005t')  # FK

class SapTinct(db.Model):
    __tablename__ = 'sap_tinct'
    __table_args__ = (
        db.ForeignKeyConstraint(['caps_gen_id'], ['caps_gen.id'], ondelete='CASCADE'),
    )
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    data = db.Column(postgresql.JSON, nullable=False)

    caps_gen_id = db.Column(db.Integer, nullable=False)  # FK
    saptinct_caps_gen = db.relationship('CapsGen', back_populates='caps_gen_saptinct')  # FK
