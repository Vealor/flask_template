import pandas as pd

# Define the preprocessing routine here
def preprocessing_train(df,**kwargs):
    # Drop the pare down data and code columns, do one-hot encoding, remove duplicate columns.
    THRESHOLD_DROP_ROWS = 2
    df = df.dropna(thresh=THRESHOLD_DROP_ROWS)
    df = df[df['Schedule'] != 'pare down']
    df = df.drop(['Schedule'], 1)
    df['Target'] = df['Code'].apply(lambda row: 1 if (99 < row < 200) else 0)
    df = df.drop(['Code'], 1)
    low_cardinality_columns = "PRI_REPORT,SEC_REPORT,Currency,VEND_CNTRY,Tax Jurisdiction".split(',')
    try:
        for column in low_cardinality_columns:
            temp_df = pd.get_dummies(df[column], prefix=column,prefix_sep=":")
            df = pd.concat([df, temp_df], axis=1)

        df = df.drop(low_cardinality_columns, 1)
    except Exception as e:
        response['status'] = 'error'
        response['message'] = "Exception in one-hot encoding: {}.".format(str(e))
        return jsonify(response, 500)

    df = df.loc[:, ~df.columns.duplicated()]
    return df

# Define the preprocessing routine here
def preprocessing_predict(df,predictors,for_validation=False):
    # Drop the pare down data and code columns, do one-hot encoding, remove duplicate columns.
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
        print('Missing col: {}'.format(col))

    # Remove extra one-hot encoding columns that are not in predictors
    extra_cols = list(set(df_onehot.columns) - set(one_hot_predictors))
    df_onehot = df_onehot.drop(extra_cols,1)
    print('Dropped {}'.format(extra_cols))

    df = pd.concat([df,df_onehot],axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    return df
