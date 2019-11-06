import pandas as pd
from src.models import Transaction, Code

def transactions_to_dataframe(query,**kwargs):

    # Get the 'data' and 'code' field for all transactions in query and merge them into dataframe
    entries, codes = zip(*[(tr.serialize['data'],tr.gst_code) for tr in query])
    entries = pd.read_json('[' + ','.join(train_entries) + ']',orient='records')

    # Get the appropriate codes from the code table
