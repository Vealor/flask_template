# ~~~ Utils:
import datetime

#==============================================================================
# prints text with specific colours if adding to print statements
class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#===============================================================================
# Builds date object from date format "YYYY-MM-DD"
#   RETURNS:
#     - datetime object
#     - ValueError on wrong format
def get_date_obj_from_str(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return date_obj

#===============================================================================
# Checks that keys and types are in JSON input
def validate_request_data(data, validation):

    # Ensures keys in validation are all in data. Data can have excess keys.
    if [x for x in validation.keys() if not x in data.keys()]:
        raise ValueError('Request is missing required keys.')

    # Esures that the datatypes specified in validation match the types in data.
    # Example Available types:
    #   int, float, bool, str, list, tuple, dict, class, object
    if [x for x in validation.keys() if not isinstance(data[x], eval(validation[x]))]:
        raise ValueError('Request contains improper data types for keys.')

#===============================================================================
#




#
