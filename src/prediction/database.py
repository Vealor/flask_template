import pandas as pd
from src.models import Transaction, Code

def transactions_to_dataframe(query,**kwargs):

    # Get the 'data' and 'code' field for all transactions in query and merge them into dataframe
    entries, codes = zip(*[(tr.serialize['data'],(tr.gst_code.code_number if tr.gst_code else -999)) for tr in query])
    entries = pd.read_json('[' + ','.join(entries) + ']',orient='records')
    entries['Code'] = codes

    return entries
