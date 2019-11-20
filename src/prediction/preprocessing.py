import os
import pandas as pd
from functools import reduce
from src.models import Transaction, Code


# ============================================================================ #
# Configuration :
PREDICTION_VARS = {
    'broker_value': 'float',
    'ccy': 'str',
    'cn_flag_ind': 'Int64',
    'cntry_name': 'str',
    'eff_rate': 'float',
    'ap_amt': 'float',
    'po_tx_jur': 'str',
    'transaction_attributes': 'list'
}

# ============================================================================ #
# Take a sqlalchemy query to the transaction table and return the transactions in a dataframe
def transactions_to_dataframe(query,**kwargs):

    # Get the 'data' and 'code' field for all transactions in query and merge them into dataframe
    #entries, codes = zip(*[(tr.serialize['data'],(tr.gst_code.code_number if tr.gst_code else -999)) for tr in query])
    print("\t serialize...")
    entries = [tr.predictive_serialize for tr in query]
    print("\t parse...")
    data = [entry['data'] for entry in entries]
    codes = [entry['codes'] for entry in entries]
    print("\t put into dataframe...")
    df = pd.DataFrame(data)
    codes_df = pd.DataFrame(codes)
    codes_df.rename(columns={x:x+"_codes" for x in codes_df.columns},inplace=True)

    return df.join(codes_df)


# Define the preprocessing routine here
def preprocess_data(df,preprocess_for='training',**kwargs):

    # Ensure that the preprocess_for variable is set to one of the correct values
    assert preprocess_for in ['training','validation','prediction']

    # If appropriate, create the code columns
    if preprocess_for in ['training','validation']:
        code_cols = list(set([x+"_codes" for x in ['gst','hst','qst','pst','apo']]) & set(df.columns))
        has_recoverable = lambda code_list: True if any((99 < code < 200) for code in code_list) else False
        df_target = pd.DataFrame({'Target':1*df[code_cols].applymap(lambda d: d if isinstance(d, list) else []).applymap(has_recoverable).any(axis=1)})
        df = df.drop(code_cols, axis = 1)

    # Ensure that the appropriate arguments are specified in the keywords
    if preprocess_for in ['validation','prediction']:
        if not kwargs['predictors']:
            raise Exception("keyword argument 'predictors' must be specified to do validation or prediction.")
        train_predictors = kwargs['predictors']
        print(train_predictors)

    # Filter the inputs to use only the predictors we want at the moment
    df = df[[x for x in df.columns if x in PREDICTION_VARS.keys()]]
    if preprocess_for in ['validation','prediction']:
        df = df[list(set(df.columns) & set(train_predictors))]

    # If training, only consider columns that have informative content
    if preprocess_for == 'training':
        informative_columns = [col for col in df.columns if df[col].nunique() > 1]
        df = df[informative_columns]

    # Enforce the data types here.
    list_columns = []
    for col in df.columns:
        imposed_type = PREDICTION_VARS[col]
        if imposed_type == 'datetime':
            df[col] = pd.to_datetime(df[col],format='%Y%m%d', errors='coerce')
        elif imposed_type == 'list':
            list_columns.append(col)
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
        str_columns = [col for col in str_columns if df[col].nunique() < 8 and col != 'transaction_attributes']

    # Only keep the data columns that we can hvaev appropriately treated

    predictors = int_columns + str_columns + float_columns + datetime_columns + list_columns
    df_final = df[predictors]

    # Do one hot encoding on the low cardinality columns
    encoded_cols = [col for col in predictors if col in int_columns + str_columns]
    for column in encoded_cols:
        temp_df = pd.get_dummies(df[column], prefix=column, prefix_sep=":", dummy_na=True)
        df_final = pd.concat([df_final, temp_df], axis=1)
    df_final = df_final.drop(encoded_cols, 1)

    # Process the transaction attributes, if they exist in the data
    if 'transaction_attributes' in df.columns:
        df_attributes = df['transaction_attributes'].str.split(",")
        l = df_attributes.apply(lambda x: [xx.strip() for xx in x])
        attribs = reduce(lambda a,b : set(a) | set(b), l)
        df_attributes = pd.DataFrame([{'transaction_attributes:{}'.format(attrib): 1*(attrib in x) for attrib in attribs} for x in l])
        df_final.drop('transaction_attributes',axis=1,inplace=True)
        df_final = df_final.join(df_attributes)

    # If validating or predicting, need to ensure all predictors are there.
    if preprocess_for in ['validation','prediction']:

        # Remove those columns that are not in the training predictors, but are in the data here.
        missing_cols = list(set(df_final.columns) - set(train_predictors))
        df_final.drop(missing_cols,axis=1,inplace=True)

        # Add those columns that are in the training predictors, but not in the columns here.
        cols_to_add = list(set(train_predictors) - set(df_final.columns))
        for col in cols_to_add:
            df_final[col] = 0

    df_final.fillna(-999,inplace=True)

    # Ensure that the data is returned with consistent column ordering

    if preprocess_for != 'training':
        print(train_predictors)
        df_final = df_final[train_predictors]
    if preprocess_for != 'prediction':
        df_final = df_final.join(df_target)
    return df_final
