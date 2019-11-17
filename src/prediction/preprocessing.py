import pandas as pd
from src.models import Transaction, Code
import os

# ============================================================================ #
# Configuration :
PREDICTION_VARS = set([
    'ccy',
    'po_tx_jur',
    'amount_local_ccy',
    'fx_rate',
    'gst_hst_qst_pst_local_ccy'
    ])

# ============================================================================ #
# Take note of the data types and mapping of variables (THIS IS LIKELY TO BE TEMPORARY)
def get_data_types():

    data_types = pd.read_csv('./src/prediction/data_types.csv', sep=',')
    data_types[['table_name','column_name']] = data_types["Data Field"].str.split(".", expand = True)
    data_types = data_types.drop('Data Field',axis=1)

    data_mapping = pd.read_csv('./src/prediction/data_mappings.csv', sep=',')

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
    #entries, codes = zip(*[(tr.serialize['data'],(tr.gst_code.code_number if tr.gst_code else -999)) for tr in query])
    entries = [tr.predictive_serialize for tr in query]
    data = [entry['data'] for entry in entries]
    codes = [entry['codes'] for entry in entries]

    df = pd.read_json('[' + ','.join(data) + ']',orient='records')
    codes_df = pd.DataFrame(codes)
    codes_df.rename(columns={x:x+"_codes" for x in codes_df.columns},inplace=True)

    return df.join(codes_df)


# Define the preprocessing routine here
def preprocess_data(df,preprocess_for='training',**kwargs):

    # Ensure that the preprocess_for variable is set to one of the correct values
    assert preprocess_for in ['training','validation','prediction']

    if preprocess_for in ['training','validation']:
        df_target = pd.DataFrame({'Target':df['Code'].apply(lambda x: 1 if (99 < x < 200) else 0)})
        df = df.drop(['Code'], axis = 1)

    # Filter the inputs to use only the predictors we want at the moment

    data_types = get_data_types()
    cols = [x for x in df.columns if x in set(data_types['cdm_label_script_label']) & PREDICTION_VARS]
    df = df[cols]

    # If training, only consider columns that have informative content
    if preprocess_for == 'training':
        informative_columns = [col for col in df.columns if df[col].nunique() > 1]
        df = df[informative_columns]

    # Enforce the data types here.
    for col in df.columns:
        print("\t{}".format(col))
        imposed_type = data_types.loc[data_types['cdm_label_script_label'] == col].iloc[0]['data_type']
        if imposed_type == 'datetime':
            df[col] = pd.to_datetime(df[col],format='%Y%m%d', errors='coerce')
        else:
            df[col] = df[col].astype(imposed_type)
            if imposed_type == 'str':
                df[col] = df[col].astype(imposed_type).replace('nan','')

    int_columns = [col for col in df.columns if df[col].dtype == 'Int64']
    str_columns = [col for col in df.columns if df[col].dtype == 'object']
    float_columns = [col for col in df.columns if df[col].dtype == 'float64']
    datetime_columns = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']


    # If training, only consider categorical columns with low cardinality
    if preprocess_for == 'training':
        int_columns = [col for col in int_columns if df[col].nunique() < 8]
        str_columns = [col for col in str_columns if df[col].nunique() < 8]

    predictors = list(set(['ccy','po_tx_jur','amount_local_ccy','fx_rate','gst_hst_qst_pst_local_ccy']) & set(df.columns))

    df_final = df[predictors]


    # Do one hot encoding on the low cardinality columns
    encoded_cols = [col for col in predictors if col in int_columns + str_columns]
    for column in encoded_cols:
        temp_df = pd.get_dummies(df[column], prefix=column, prefix_sep=":", dummy_na=True)
        df_final = pd.concat([df_final, temp_df], axis=1)
    df_final = df_final.drop(encoded_cols, 1)

    # If validating or predicting, need to ensure all predictors are there.
    if preprocess_for in ['validation','prediction']:

        train_predictors = kwargs['predictors']

        # Remove those columns that are not in the training predictors, but are in the data here.
        missing_cols = list(set(df_final.columns) - set(train_predictors))
        df_final.drop(missing_cols,axis=1,inplace=True)

        # Add those columns that are in the training predictors, but not in the columns here.
        cols_to_add = list(set(train_predictors) - set(df_final.columns))
        for col in cols_to_add:
            df_final[col] = 0

    df_final.fillna(-999,inplace=True)

    if preprocess_for in ['training','validation']:
        return df_final.join(df_target)
    return df_final

# Define the preprocessing routine here
# def preprocessing_predict(df,train_predictors,for_validation=False):
#
#     if for_validation:
#         df_target = pd.DataFrame({'Target':df['Code'].apply(lambda x: 1 if (99 < x < 200) else 0)})
#     df = df.drop(['Code'], axis = 1)
#
#     data_types = get_data_types()
#     cols = [x for x in df.columns if x in set(data_types['cdm_label_script_label'])]
#     df = df[cols]
#
#     # Enforce the data types here.
#     for col in df.columns:
#         imposed_type = data_types.loc[data_types['cdm_label_script_label'] == col].iloc[0]['data_type']
#         if imposed_type == 'datetime':
#             df[col] = pd.to_datetime(df[col],format='%Y%m%d', errors='coerce')
#         else:
#             df[col] = df[col].astype(imposed_type)
#             if imposed_type == 'str':
#                 df[col] = df[col].astype(imposed_type).replace('nan','')
#
#     int_columns = [col for col in df.columns if (df[col].dtype == 'Int64')]
#     str_columns = [col for col in df.columns if (df[col].dtype == 'object')]
#     float_columns = [col for col in df.columns if df[col].dtype == 'float64']
#     datetime_columns = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']
#
#     predictors = ['ccy','po_tx_jur','amount_local_ccy','fx_rate','gst_hst_qst_pst_local_ccy']
#     df_final = df[predictors]
#     # Do one hot encoding on the low cardinality columns
#     encoded_cols = [col for col in predictors if col in int_columns + str_columns]
#     for column in encoded_cols:
#         temp_df = pd.get_dummies(df[column], prefix=column, prefix_sep=":", dummy_na=True)
#         df_final = pd.concat([df_final, temp_df], axis=1)
#     df_final = df_final.drop(encoded_cols, 1)
#
#     # Remove those columns that are not in the training predictors, but are in the data here.
#     missing_cols = list(set(df_final.columns) - set(train_predictors))
#     df_final.drop(missing_cols,axis=1,inplace=1)
#
#     # Add those columns that are in the training predictors, but not in the columns here.
#     cols_to_add = list(set(train_predictors) - set(df_final.columns))
#     for col in cols_to_add:
#         df_final[col] = 0
#
#     # Fill the NaN columns with a large negative value
#     df_final.fillna(-999,inplace=True)
#     if for_validation:
#         return df_final.join(df_target)
#     return df_final
