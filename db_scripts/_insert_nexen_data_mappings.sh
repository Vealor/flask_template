#!/bin/bash

PGPASSWORD=LHDEV1234 psql -h localhost -U itra itra_db -c "
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','BELNR',1,'bkpf_belnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','BLART',1,'doc_type_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','BLDAT',1,'inv_date');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','BUDAT',1,'post_date_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','BUKRS',1,'bkpf_bukrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','GJAHR',1,'bkpf_gjahr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','KURSF',1,'fx_rate');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','KZWRS',1,'bkpf_kzwrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','MONAT',1,'fiscal_period_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','TCODE',1,'trnx_code_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','WAERS',1,'ccy');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BKPF','XBLNR',1,'inv_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','AUGBL',1,'bsak_augbl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','AUGDT',1,'bsak_augdt_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','BELNR',1,'bsak_belnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','BUKRS',1,'bsak_bukrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','BUZEI',1,'bsak_buzei_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','GJAHR',1,'bsak_gjahr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','LIFNR',1,'bsak_lifnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','UMSKS',1,'spec_trnx_type_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','UMSKZ',1,'spec_indicator_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZBD1P',1,'cash_disc_percent_1_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZBD1T',1,'cash_disc_days_1_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZBD2P',1,'cash_disc_percent_2_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZBD2T',1,'cash_disc_days_2_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZBD3T',1,'pymt_period_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZTERM',1,'pymt_terms_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSAK','ZUONR',1,'assign_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','ANLN1',1,'main_asset_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','ANLN2',1,'asset_sub_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','BELNR',1,'gl_doc_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','BSCHL',1,'post_key_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','BSTAT',1,'gl_doc_status');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','BUDAT',1,'bseg_budat_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','BUKRS',1,'co_code_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','BUZEI',1,'bseg_buzei_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','DMBTR',1,'amount_local_ccy');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','EBELN',1,'po_doc_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','EBELP',1,'bseg_ebelp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','FKBER',1,'func_area_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','GJAHR',1,'fiscal_year_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','GSBER',1,'bus_area_dept_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','HKONT',1,'largest_debit_half_acct_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','KOKRS',1,'control_area_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','KOSTL',1,'cost_ctr_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','KUNNR',1,'cx_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','LIFNR',1,'vend_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','MATNR',1,'material_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','MWART',1,'tax_type_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','MWSK3',1,'bseg_mwsk3_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','MWSKZ',1,'po_tax_code_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','MWSTS',1,'gst_hst_qst_pst_local_ccy');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','PARGB',1,'bseg_pargb_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','PRCTR',1,'profit_ctr_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','PROJK',1,'wbs_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','SGTXT',1,'item_descr_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','STBLG',1,'reverse_doc_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','STGRD',1,'reverse_reason_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','TXJCD',1,'tax_jur_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','VBEL2',1,'sales_doc_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','VBELN',1,'billing_doc_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','WMWST',1,'gst_hst_pst_qst_doc_ccy');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('BSEG','WRBTR',1,'ap_ar_amt_doc_ccy');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPC','DATBI',1,'cepc_datbi_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPC','KOKRS',1,'cepc_kokrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPC','PRCTR',1,'cepc_prctr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPC','TXJCD',1,'profit_ctr_tx_jur');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPCT','KTEXT',1,'profit_ctr_name');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPCT','LTEXT',1,'profit_ctr_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPCT','PRCTR',1,'cepct_prctr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CEPCT','SPRAS',1,'cepct_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKS','DATBI',1,'csks_datbi_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKS','KOKRS',1,'csks_kokrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKS','KOSTL',1,'csks_kostl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKS','TXJCD',1,'cost_ctr_tx_jur');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKT','DATBI',1,'cskt_datbi_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKT','KOKRS',1,'cskt_kokrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKT','KOSTL',1,'cskt_kostl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKT','KTEXT',1,'cost_ctr_name');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKT','LTEXT',1,'cost_ctr_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('CSKT','SPRAS',1,'cskt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKA1','BUKRS',1,'ska1_bukrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKA1','KTOPL',1,'ska1_ktopl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKA1','SAKNR',1,'ska1_saknr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKAT','KTOPL',1,'skat_ktopl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKAT','SAKNR',1,'skat_saknr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKAT','SPRAS',1,'skat_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKAT','TXT50',1,'lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKB1','BUKRS',1,'skb1_bukrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('SKB1','SAKNR',1,'skb1_saknr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T003T','BLART',1,'t003t_blart_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T003T','LTEXT',1,'doc_type_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T003T','SPRAS',1,'t003t_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TBSLT','BSCHL',1,'tbslt_bschl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TBSLT','LTEXT',1,'post_key_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TBSLT','SPRAS',1,'tbslt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TBSLT','UMSKZ',1,'tbslt_umskz_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TCURT','KTEXT',1,'ccy_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TCURT','SPRAS',1,'tcurt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TCURT','WAERS',1,'tcurt_waers_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TGSBT','GSBER',1,'tgsbt_gsber_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TGSBT','GTEXT',1,'bus_area_dept_name_gl');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TGSBT','SPRAS',1,'tgsbt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKKO','EBELN',1,'ekko_ebeln_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKKO','EKGRP',1,'punch_grp_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKKO','EKORG',1,'punch_org_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKKO','HANDOVERLOC',1,'handover_loc_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKKO','TELF1',1,'vend_phone');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKKO','VERKF',1,'vend_person');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','DISUB_PSPNR',1,'wbs_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','EBELN',1,'ekpo_ebeln_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','EBELP',1,'ekpo_ebelp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','EMATN',1,'ekpo_ematn_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','LGORT',1,'ekpo_lgort_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','MWSKZ',1,'po_tx_code_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','WERKS',1,'plant_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','TXJCD',1,'po_tx_jur');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('EKPO','TXZ01',1,'po_item_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','LAND1',1,'lfa1_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','LIFNR',1,'lfa1_lifnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','NAME1',1,'vend_name');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','ORT01',1,'vend_city');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','REGIO',1,'vend_region');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCD1',1,'vend_tax_num_1');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCD2',1,'vend_tax_num_2');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCD3',1,'vend_tax_num_3');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCD4',1,'vend_tax_num_4');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCD5',1,'vend_tax_num_5');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCDT',1,'vend_tax_num_type');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFA1','STCEG',1,'vend_reg_num');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFAS','LAND1',1,'lfas_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFAS','LIFNR',1,'lfas_lifnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFM1','EKORG',1,'lfm1_ekorg_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFM1','INCO1',1,'incoterms1');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFM1','INCO2',1,'incoterms2');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('LFM1','LIFNR',1,'lfm1_lifnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T024','EKGRP',1,'t024_ekgrp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T024','EKNAM',1,'purch_group_descr_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T024E','EKORG',1,'t024e_ekorg_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T024E','EKOTX',1,'purch_org_descr_po');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TOA01','ARC_DOC_ID',1,'toa01_arc_doc_id_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TOA01','ARCHIV_ID',1,'toa01_archiv_id_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TOA01','OBJECT_ID',1,'toa01_object_id_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TOA01','SAP_OBJECT',1,'toa01_sap_object_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MAKT','MAKTX',1,'mat_descr_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MAKT','MATNR',1,'makt_matnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','EAN11',1,'ean_upc_num_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','GEWEI',1,'mara_gewei_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','HERKL',1,'mat_orig_ctry_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','MAGRV',1,'mara_magrv_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','MATKL',1,'mara_matkl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','MATNR',1,'mara_matnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','MFRNR',1,'mara_mfrnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','NUMTP',1,'ean_categ_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','TAKLV',1,'mat_tx_class_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MARA','VOLEH',1,'mara_voleh_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MLAN','ALAND',1,'mat_dept_ctry_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MLAN','MATNR',1,'mlan_matnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MLAN','TAXIM',1,'mat_tx_ind_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MSEG','EBELN',1,'mseg_ebeln_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MSEG','EBELP',1,'mseg_ebelp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MSEG','MBLNR',1,'mat_doc_num_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MSEG','MJAHR',1,'mseg_mjahr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MSEG','WERKS',1,'mat_plnt_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('MSEG','ZEILE',1,'mseg_zeile_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001L','LGOBE',1,'stor_loc_desc_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001L','LGORT',1,'stor_loc_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001L','WERKS',1,'stor_plant_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T006A','MSEHI',1,'t006a_msehi_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T006A','SPRAS',1,'t006a_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T023T','MATKL',1,'t023t_matkl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T023T','SPRAS',1,'t023t_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T023T','WGBEZ',1,'mat_group_descr_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TMKM1T','LAND1',1,'tmkm1t_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TMKM1T','SPRAS',1,'tmkm1t_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TMKM1T','TAXIB',1,'mat_tx_ind_descr_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TNTPB','NTBEZ',1,'ean_categ_descr_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TNTPB','NUMTP',1,'tntpb_numtp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TNTPB','SPRAS',1,'tntpb_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TSKMT','SPRAS',1,'tskmt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TSKMT','TATYP',1,'tskmt_tatyp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TSKMT','TAXKM',1,'tskmt_taxkm_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TSKMT','VTEXT',1,'mat_tx_class_descr_mat');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TVEGRT','SPRAS',1,'tvegrt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TVTYT','SPRAS',1,'tvtyt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TVTYT','TRATY',1,'tvtyt_traty_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','POST1',1,'proj_descr_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','PSPID',1,'proj_defin_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','PSPNR',1,'proj_internal_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','TXJCD',1,'proj_tx_jur_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','VERNA',1,'proj_mngr_name_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','VERNR',1,'proj_mngr_num_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','VGSBR',1,'bus_area_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PROJ','WERKS',1,'plant_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','OBJNR',1,'object_num_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','OTYPE',1,'jv_obj_type_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','PGSBR',1,'wbs_bus_area_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','PKOKR',1,'wbs_cntrl_area_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','POSID',1,'wbs_elem_id_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','POST1',1,'wbs_elem_descr_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','PRART',1,'proj_type_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','PSPHI',1,'prps_psphi_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','PSPNR',1,'prps_pspnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PRPS','STORT',1,'proj_loc_proj');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PAYR','CHECT',1,'check_num_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PAYR','HBKID',1,'payr_hbkid_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PAYR','RZAWE',1,'payr_rzawe_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PAYR','ZALDT',1,'pymt_dt_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('PAYR','ZBUKR',1,'payr_zbukr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','BELNR',1,'pymt_doc_num_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','BUKRS',1,'regup_bukrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','BUZEI',1,'regup_buzei_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','EBELN',1,'regup_ebeln_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','EBELP',1,'regup_ebelp_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','EMPFG',1,'payee_code_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','GJAHR',1,'regup_gjahr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','HKONT',1,'regup_hkont_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','KUNNR',1,'cx_num_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','LAUFD',1,'regup_laufd_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','LAUFI',1,'regup_laufi_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','LIFNR',1,'regup_lifnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','SAKNR',1,'regup_saknr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','VBLNR',1,'regup_vblnr_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','XVORL',1,'regup_xvorl_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','ZBUKR',1,'co_code_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('REGUP','ZLSCH',1,'regup_zlsch_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T042ZT','LAND1',1,'t042zt_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T042ZT','SPRAS',1,'t042zt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T042ZT','TEXT2',1,'pymt_method_pmt');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T042ZT','ZLSCH',1,'t042zt_zlsch_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('J_1ATODCT','J_1ATODCT',1,'j_1atodct_j_1atodct_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('J_1ATODCT','SPRAS',1,'j_1atodct_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('J_1ATODCT','TEXT30',1,'tx_type_descr_tx');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T005S','BLAND',1,'t005s_bland_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T005S','FPRCD',1,'prov_tx_code_tx');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T005S','LAND1',1,'t005s_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T007A','KALSM',1,'t007a_kalsm_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T007A','MWSKZ',1,'t007a_mwskz_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T007S','KALSM',1,'t007s_kalsm_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T007S','MWSKZ',1,'t007s_mwskz_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T007S','SPRAS',1,'t007s_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T007S','TEXT1',1,'tx_name_tx');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TTXJT','KALSM',1,'ttxjt_kalsm_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TTXJT','SPRAS',1,'ttxjt_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TTXJT','TEXT1',1,'tx_jur_descr_tx');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TTXJT','TXJCD',1,'ttxjt_txjcd_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001','BUKRS',1,'t001_bukrs_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001','BUTXT',1,'co_name');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001','LAND1',1,'t001_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001W','NAME1',1,'plant_name_plant');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001W','TXJCD',1,'plant_tx_jur_plant');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T001W','WERKS',1,'t001w_werks_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T005T','LAND1',1,'t005t_land1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T005T','LANDX',1,'cntry_name');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('T005T','SPRAS',1,'t005t_spras_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TINCT','BEZEI',1,'incoterms1_descr');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TINCT','INCO1',1,'tinct_inco1_key');
  INSERT INTO data_mappings(table_name,column_name,caps_gen_id,cdm_label_script_label) VALUES ('TINCT','SPRAS',1,'tinct_spras_key');
  INSERT INTO sap_aufk(caps_Gen_id, data) VALUES (2,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_bkpf(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_bsak(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_bsak(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_bseg(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_bseg(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_cepct(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_cepct(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_csks(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_csks(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_cskt(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_cskt(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_ekko(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_ekko(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_ekpo(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_ekpo(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_iflot(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_iflot(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_iloa(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_iloa(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_lfa1(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_lfa1(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_makt(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_makt(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_mara(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_mara(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_payr(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_payr(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_proj(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_proj(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_prps(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_prps(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_regup(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_regup(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_skat(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_skat(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_t001(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_t001(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_t007s(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_t007s(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_skb1(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
  INSERT INTO sap_skb1(caps_gen_id, data) VALUES (1,'{\"vegie\": \"tomato\",\"color\": \"red\"}');
  INSERT INTO sap_t003t(caps_gen_id, data) VALUES (1,'{\"vegie\": \"potato\",\"color\": \"brown\"}');
"
