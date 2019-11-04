#!/bin/bash

PGPASSWORD=LHDEV1234 psql -h localhost -U itra itra_db -c "
  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (1, 'Acct_Desc', 'contains', 'Donation');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (2, 'Item_Text', 'contains', 'Donation');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (3, 'INVOICE_NUM', 'contains', 'Donation');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (4, 'Acct_Desc', 'contains', 'Sponsorship');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (5, 'Item_Text', 'contains', 'Sponsorship');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (6, 'INVOICE_NUM', 'contains', 'Sponsorship');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (7, 'Acct_Desc', 'contains', 'Charity');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (8, 'Item_Text', 'contains', 'Charity');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (9, 'INVOICE_NUM', 'contains', 'Charity');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (10, 'Acct_Desc', 'contains', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (10, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (11, 'Item_Text', 'contains', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (11, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (12, 'INVOICE_NUM', 'contains', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (12, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (13, 'Acct_Desc', 'contains', 'Health');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (13, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (14, 'Item_Text', 'contains', 'Health');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (14, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (15, 'INVOICE_NUM', 'contains', 'Health');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (15, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (16, 'Acct_Desc', 'contains', 'Dental');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (16, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (17, 'Item_Text', 'contains', 'Dental');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (17, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (18, 'INVOICE_NUM', 'contains', 'Dental');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (18, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (19, 'Acct_Desc', 'contains', 'Disability');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (19, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (20, 'Item_Text', 'contains', 'Disability');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (20, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (21, 'INVOICE_NUM', 'contains', 'Disability');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (21, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (22, 'Acct_Desc', 'contains', 'LTD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (22, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (23, 'Item_Text', 'contains', 'LTD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (23, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (24, 'INVOICE_NUM', 'contains', 'LTD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (24, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (25, 'Acct_Desc', 'contains', 'STD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (25, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (26, 'Item_Text', 'contains', 'STD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (26, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (27, 'INVOICE_NUM', 'contains', 'STD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (27, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (28, 'Acct_Desc', 'contains', 'Medical');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (28, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (29, 'Item_Text', 'contains', 'Medical');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (29, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (30, 'INVOICE_NUM', 'contains', 'Medical');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (30, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (31, 'Acct_Desc', 'contains', 'Medical Services Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (31, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (32, 'Item_Text', 'contains', 'Medical Services Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (32, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (33, 'Acct_Desc', 'contains', 'MSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (33, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (34, 'Item_Text', 'contains', 'MSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (34, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (35, 'INVOICE_NUM', 'contains', 'MSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (35, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (36, 'Acct_Desc', 'contains', 'Payroll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (36, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (37, 'Item_Text', 'contains', 'Payroll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (37, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (38, 'INVOICE_NUM', 'contains', 'Payroll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (38, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (39, 'Acct_Desc', 'contains', 'Salary');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (39, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (40, 'Item_Text', 'contains', 'Salary');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (40, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (41, 'INVOICE_NUM', 'contains', 'Salary');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (41, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (42, 'Acct_Desc', 'contains', 'Salaries');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (42, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (43, 'Item_Text', 'contains', 'Salaries');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (43, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (44, 'INVOICE_NUM', 'contains', 'Salaries');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (44, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (45, 'Acct_Desc', 'contains', 'Severance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (45, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (46, 'Item_Text', 'contains', 'Severance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (46, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (47, 'INVOICE_NUM', 'contains', 'Severance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (47, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (48, 'Acct_Desc', 'contains', 'Employment insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (48, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (49, 'Item_Text', 'contains', 'Employment insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (49, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (50, 'Acct_Desc', 'contains', 'Employer Health Tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (50, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (51, 'Item_Text', 'contains', 'Employer Health Tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (51, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (52, 'Acct_Desc', 'contains', 'EHT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (52, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (53, 'Item_Text', 'contains', 'EHT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (53, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (54, 'INVOICE_NUM', 'contains', 'EHT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (54, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (55, 'Acct_Desc', 'contains', 'Garnish');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (55, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (56, 'Item_Text', 'contains', 'Garnish');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (56, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (57, 'INVOICE_NUM', 'contains', 'Garnish');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (57, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (58, 'Acct_Desc', 'contains', 'Share purchase');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (58, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (59, 'Item_Text', 'contains', 'Share purchase');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (59, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (60, 'Acct_Desc', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (60, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (61, 'Item_Text', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (61, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (62, 'INVOICE_NUM', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (62, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (63, 'Acct_Desc', 'contains', 'RRSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (63, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (64, 'Item_Text', 'contains', 'RRSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (64, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (65, 'INVOICE_NUM', 'contains', 'RRSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (65, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (66, 'Acct_Desc', 'contains', 'Work Safety');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (66, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (67, 'Item_Text', 'contains', 'Work Safety');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (67, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (68, 'Acct_Desc', 'contains', 'Workers Comp');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (68, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (69, 'Item_Text', 'contains', 'Workers Comp');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (69, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (70, 'Acct_Desc', 'contains', 'workers compensation board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (70, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (71, 'Item_Text', 'contains', 'workers compensation board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (71, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (72, 'Acct_Desc', 'contains', 'Worksafe BC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (72, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (73, 'Item_Text', 'contains', 'Worksafe BC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (73, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (74, 'Acct_Desc', 'contains', 'WorksafeBC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (74, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (75, 'Item_Text', 'contains', 'WorksafeBC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (75, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (76, 'Acct_Desc', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (76, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (77, 'Item_Text', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (77, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (78, 'INVOICE_NUM', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (78, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (79, 'Acct_Desc', 'contains', 'WSIB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (79, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (80, 'Item_Text', 'contains', 'WSIB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (80, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (81, 'INVOICE_NUM', 'contains', 'WSIB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (81, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (82, 'Acct_Desc', 'contains', 'Workplace Safety & Insurance Board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (82, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (83, 'Item_Text', 'contains', 'Workplace Safety & Insurance Board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (83, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (84, 'Acct_Desc', 'contains', 'Canada Pension Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (84, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (85, 'Item_Text', 'contains', 'Canada Pension Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (85, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (86, 'Acct_Desc', 'contains', 'WCB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (86, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (87, 'Item_Text', 'contains', 'WCB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (87, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (88, 'INVOICE_NUM', 'contains', 'WCB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (88, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (89, 'Acct_Desc', 'contains', 'Union due');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (89, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (90, 'Item_Text', 'contains', 'Union due');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (90, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (91, 'Acct_Desc', 'contains', 'Pension');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (91, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (92, 'Item_Text', 'contains', 'Pension');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (92, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (93, 'INVOICE_NUM', 'contains', 'Pension');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (93, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (94, 'Acct_Desc', 'contains', 'Dividends');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (94, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (95, 'Item_Text', 'contains', 'Dividends');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (95, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (96, 'INVOICE_NUM', 'contains', 'Dividends');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (96, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (97, 'Acct_Desc', 'contains', 'EI ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (97, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (98, 'Item_Text', 'contains', 'EI ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (98, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (99, 'Acct_Desc', 'contains', 'CPP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (99, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (100, 'Item_Text', 'contains', 'CPP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (100, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (101, 'INVOICE_NUM', 'contains', 'CPP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (101, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (102, 'Acct_Desc', 'contains', 'Loan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (102, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (103, 'Item_Text', 'contains', 'Loan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (103, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (104, 'INVOICE_NUM', 'contains', 'Loan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (104, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (105, 'Acct_Desc', 'contains', 'Debt');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (105, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (106, 'Item_Text', 'contains', 'Debt');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (106, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (107, 'INVOICE_NUM', 'contains', 'Debt');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (107, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (108, 'Acct_Desc', 'contains', 'Interest');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (108, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (109, 'Item_Text', 'contains', 'Interest');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (109, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (110, 'INVOICE_NUM', 'contains', 'Interest');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (110, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Tolls');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (111, 'Acct_Desc', 'contains', 'Toll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (111, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Tolls');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (112, 'Item_Text', 'contains', 'Toll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (112, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (113, 'INVOICE_NUM', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (113, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (113, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (114, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (114, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (114, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (115, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (115, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (115, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (116, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (116, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (116, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (117, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (117, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (117, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (118, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (118, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (118, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (119, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (119, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (119, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (120, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (120, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (120, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (121, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (121, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (121, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (122, 'INVOICE_NUM', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (122, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (122, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (123, 'Acct_Desc', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (123, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (123, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (124, 'Item_Text', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (124, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (124, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (125, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (125, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (125, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (126, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (126, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (126, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (127, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (127, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (127, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (128, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (128, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (128, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (129, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (129, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (129, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (130, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (130, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (130, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (131, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (131, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (131, 'Acct_Desc', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (132, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (132, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (132, 'Item_Text', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (133, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (133, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (133, 'INVOICE_NUM', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (134, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (134, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (134, 'Acct_Desc', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (135, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (135, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (135, 'Item_Text', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (136, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (136, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (136, 'INVOICE_NUM', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (137, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (137, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (137, 'Acct_Desc', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (138, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (138, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (138, 'Item_Text', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (139, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (139, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (139, 'INVOICE_NUM', 'contains', 'CT ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (140, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (140, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (140, 'Acct_Desc', 'contains', 'CT ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (141, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (141, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (141, 'Item_Text', 'contains', 'CT ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (142, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (142, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (142, 'INVOICE_NUM', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (143, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (143, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (143, 'Acct_Desc', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (144, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (144, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (144, 'Item_Text', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (145, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (145, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (145, 'INVOICE_NUM', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (146, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (146, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (146, 'Acct_Desc', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (147, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (147, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (147, 'Item_Text', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (148, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (148, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (148, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (149, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (149, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (149, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (150, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (150, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (150, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (151, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (151, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (151, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (152, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (152, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (152, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (153, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (153, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (153, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (154, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (154, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (154, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (155, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (155, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (155, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (156, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (156, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (156, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (157, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (157, 'INVOICE_NUM', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (157, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (158, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (158, 'Acct_Desc', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (158, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (159, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (159, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (159, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (160, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (160, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (160, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (161, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (161, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (161, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (162, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (162, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (162, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (163, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (163, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (163, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (164, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (164, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (164, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (165, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (165, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (165, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (166, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (166, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (166, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (167, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (167, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (167, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (168, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (168, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (168, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (169, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (169, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (169, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (170, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (170, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (170, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (171, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (171, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (171, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (172, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (172, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (172, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (173, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (173, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (173, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (174, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (174, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (174, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (175, 'INVOICE_NUM', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (175, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (175, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (176, 'Acct_Desc', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (176, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (176, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (177, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (177, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (177, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (178, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (178, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (178, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (179, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (179, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (179, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (180, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (180, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (180, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (181, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (181, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (181, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (182, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (182, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (182, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (183, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (183, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (183, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (184, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (184, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (184, 'Acct_Desc', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (185, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (185, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (185, 'Item_Text', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (186, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (186, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (186, 'INVOICE_NUM', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (187, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (187, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (187, 'Acct_Desc', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (188, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (188, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (188, 'Item_Text', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (189, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (189, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (189, 'INVOICE_NUM', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (190, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (190, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (190, 'Acct_Desc', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (191, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (191, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (191, 'Item_Text', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (192, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (192, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (192, 'INVOICE_NUM', 'contains', 'CT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (193, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (193, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (193, 'Acct_Desc', 'contains', 'CT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (194, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (194, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (194, 'Item_Text', 'contains', 'CT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (195, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (195, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (195, 'INVOICE_NUM', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (196, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (196, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (196, 'Acct_Desc', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (197, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (197, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (197, 'Item_Text', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (198, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (198, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (198, 'INVOICE_NUM', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (199, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (199, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (199, 'Acct_Desc', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (200, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (200, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (200, 'Item_Text', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (201, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (201, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (201, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (202, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (202, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (202, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (203, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (203, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (203, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (204, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (204, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (204, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (205, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (205, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (205, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (206, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (206, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (206, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (207, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (207, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (207, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (208, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (208, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (208, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (209, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (209, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (209, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (210, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (210, 'INVOICE_NUM', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (210, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (211, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (211, 'Acct_Desc', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (211, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (212, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (212, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (212, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (213, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (213, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (213, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (214, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (214, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (214, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (215, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (215, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (215, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (216, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (216, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (216, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (217, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (217, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (217, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (218, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (218, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (218, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (219, 'Acct_Desc', 'contains', 'AP amount');

"
sleep 1
