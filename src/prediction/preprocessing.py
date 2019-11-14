import pandas as pd
from src.models import Transaction, Code
import os

# ============================================================================ #
# Take note of the data types and mapping of variables (THIS IS LIKELY TO BE TEMPORARY)
def get_data_types():

    data_types = pd.read_csv('../src/prediction/data_types.csv', sep=',')
    data_types[['table_name','column_name']] = data_types["Data Field"].str.split(".", expand = True)
    data_types = data_types.drop('Data Field',axis=1)

    data_mapping = pd.read_csv('../src/prediction/data_mappings.csv', sep=',')

    data_types = pd.merge(data_mapping,data_types,on=['table_name','column_name'],how='left')
    data_types.rename(columns={"Data Type":"data_type"},inplace = True)

    # MAP the SAP data types to Python types
    data_types['data_type'].replace("CHAR","str",inplace = True)
    data_types['data_type'].replace("DEC","float",inplace = True)
    data_types['data_type'].replace("CURR","float",inplace = True)
    data_types['data_type'].replace("DATS",'datetime',inplace = True)
    data_types['data_type'].replace("NUMC",'Int64',inplace = True)
    data_types['data_type'].replace("LANG",'str',inplace = True)
    data_types['data_type'].replace("CUKY",'str',inplace = True)
    data_types['data_type'].replace("UNIT",'str',inplace = True)

    # Special cases
    data_types.loc[data_types['cdm_label_script_label'] == 'wbs_gl','data_type'] = 'str'                #(This has non-numerical characters)
    data_types.loc[data_types['cdm_label_script_label'] == 'prps_psphi_key','data_type'] = 'str'        #(This has non-numerical characters)
    data_types.loc[data_types['cdm_label_script_label'] == 'prps_pspnr_key','data_type'] = 'str'        #(This has non-numerical characters)
    data_types.loc[data_types['cdm_label_script_label'] == 'proj_internal_proj','data_type'] = 'str'    #(This has non-numerical characters)

    return data_types

# ============================================================================ #
# Take a sqlalchemy query to the transaction table and return the transactions in a dataframe
def transactions_to_dataframe(query,**kwargs):

    # Get the 'data' and 'code' field for all transactions in query and merge them into dataframe
    entries, codes = zip(*[(tr.serialize['data'],(tr.gst_code.code_number if tr.gst_code else -999)) for tr in query])
    entries = pd.read_json('[' + ','.join(entries) + ']',orient='records')
    entries['Code'] = codes

    return entries

# Define the preprocessing routine here
def preprocessing_train(df,**kwargs):

    # Pop the target column to save it for when the
    # Only look at columns that are in the data dictionary

    df_target = pd.DataFrame({'Target':df['Code'].apply(lambda x: 1 if (99 < x < 200) else 0)})
    df = df.drop(['Code'], axis = 1)

    data_types = get_data_types()
    cols = [x for x in df.columns if x in set(data_types['cdm_label_script_label'])]
    df = df[cols]

    # Only consider columns that have informative content
    informative_columns = [col for col in df.columns if df[col].nunique() > 1]
    df = df[informative_columns]

    # Enforce the data types here.
    for col in df.columns:
        imposed_type = data_types.loc[data_types['cdm_label_script_label'] == col].iloc[0]['data_type']
        if imposed_type == 'datetime':
            df[col] = pd.to_datetime(df[col],format='%Y%m%d', errors='coerce')
        else:
            df[col] = df[col].astype(imposed_type)
            if imposed_type == 'str':
                df[col] = df[col].astype(imposed_type).replace('nan','')

    int_columns = [col for col in informative_columns if (df[col].dtype == 'Int64' and df[col].nunique() < 8)]
    str_columns = [col for col in informative_columns if (df[col].dtype == 'object' and df[col].nunique() < 8)]
    float_columns = [col for col in informative_columns if df[col].dtype == 'float64']
    datetime_columns = [col for col in informative_columns if df[col].dtype == 'datetime64[ns]']

    predictors = ['ccy','po_tx_jur','amount_local_ccy','fx_rate','inv_date','gst_hst_qst_pst_local_ccy']
    df_final = df[predictors]
    # Do one hot encoding on the low cardinality columns
    encoded_cols = [col for col in predictors if col in int_columns + str_columns]
    for column in encoded_cols:
        temp_df = pd.get_dummies(df[column], prefix=column, prefix_sep=":", dummy_na=True)
        df_final = pd.concat([df_final, temp_df], axis=1)
    df_final = df_final.drop(encoded_cols, 1)
    df_final.drop('inv_date',axis=1,inplace=True)
    df_final.fillna(-999,inplace=True)

    print(df_final.columns)
    print(df_target.columns)

    return df_final.join(df_target)



    # Drop the pare down data and code columns, do one-hot encoding, remove duplicate columns.
    # THRESHOLD_DROP_ROWS = 2
    # df = df.dropna(thresh=THRESHOLD_DROP_ROWS)
    # if 'Schedule' in df.columns:
    #     df = df[df['Schedule'] != 'pare down']
    #     df = df.drop(['Schedule'], 1)
    # df['Target'] = df['Code'].apply(lambda row: 1 if (99 < row < 200) else 0)
    # df = df.drop(['Code'], 1)
    # low_cardinality_columns = "PRI_REPORT,SEC_REPORT,Currency,VEND_CNTRY,Tax Jurisdiction".split(',')
    # try:
    #     for column in low_cardinality_columns:
    #         temp_df = pd.get_dummies(df[column], prefix=column,prefix_sep=":")
    #         df = pd.concat([df, temp_df], axis=1)
    #
    #     df = df.drop(low_cardinality_columns, 1)
    # except Exception as e:
    #     response['status'] = 'error'
    #     response['message'] = "Exception in one-hot encoding: {}.".format(str(e))
    #     return jsonify(response, 500)
    #
    # df = df.loc[:, ~df.columns.duplicated()]
    return df

# Define the preprocessing routine here
def preprocessing_predict(df,predictors,for_validation=False):
    # Drop the pare down data and code columns, do one-hot encoding, remove duplicate columns.
    if 'Schedule' in df.columns:
        df = df[df['Schedule'] != 'pare down']
        df = df.drop(['Schedule'], 1)

    if for_validation:
        df['Target'] = df['Code'].apply(lambda row: 1 if (99 < row < 200) else 0)
        df = df.drop(['Code'], 1)

    low_cardinality_columns = "PRI_REPORT,SEC_REPORT,Currency,VEND_CNTRY,Tax Jurisdiction".split(',')

    df_onehot = df[low_cardinality_columns]
    one_hot_predictors = []
    for column in low_cardinality_columns:
        temp_df = pd.get_dummies(df[column], prefix=column, prefix_sep=":")
        df_onehot = pd.concat([df_onehot, temp_df], axis=1)
        one_hot_predictors.extend([pred for pred in predictors if pred[:len(column)] == column])
        df = df.drop(column,1)

    df_onehot = df_onehot.drop(low_cardinality_columns, 1)

    # Add missing one-hot encoding columns from predictors, filled with zeros
    missing_cols = list(set(one_hot_predictors) - set(df_onehot.columns))
    for col in missing_cols:
       df_onehot[col] = 0

    # Remove extra one-hot encoding columns that are not in predictors
    extra_cols = list(set(df_onehot.columns) - set(one_hot_predictors))
    df_onehot = df_onehot.drop(extra_cols,1)

    df = pd.concat([df,df_onehot],axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df
