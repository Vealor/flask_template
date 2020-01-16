# ~~~ Utils:
import datetime
import re
import sendgrid
from flask import current_app
from src.errors import InputError
from src.models import db, Actions, Log

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
# Create general system log entry
def create_log(user, action, affected_entity, details):
    if action not in Actions.__members__:
        raise Exception('Unable to generate log with the action {}.'.format(action))
    if not user:
        raise Exception('Current User does not exist to creat this log entry.')
    if len(affected_entity) > 255:
        raise Exception('Affected Entity for log has too long of string. Keep under 256.')
    db.session.add(Log(
        user_id = user.id,
        action = eval("Actions." + action),
        affected_entity = affected_entity,
        details = details
    ))
    db.session.commit()

#===============================================================================
# Builds date object from date format "YYYY-MM-DD"
#   RETURNS:
#     - datetime object
#     - InputError on wrong format
def get_date_obj_from_str(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        raise InputError("Incorrect data format, should be YYYY-MM-DD")
    return date_obj

#===============================================================================
# Checks that keys and types are in JSON input
def validate_request_data(data, validation):
    if not isinstance(data, dict):
        raise InputError('Input payload for endpoint must be a dictionary.')
    # Ensures keys in validation are all in data. Data can have excess keys.
    missing_vars = [x for x in validation.keys() if x not in data.keys()]
    if missing_vars:
        raise InputError('Request is missing required keys: {}'.format(missing_vars))

    # Esures that the datatypes specified in validation match the types in data.
    # Example Available types:
    #   int, float, bool, str, list, tuple, dict, class, object, '', NoneType
    for key in validation.keys():
        valid = False
        for datatype in validation[key]:
            if datatype == 'NoneType':
                if isinstance(data[key], (str, type(None))):
                    valid = True
            elif datatype == '':
                if data[key] == '':
                    valid = True
            elif isinstance(data[key], eval(datatype)):
                valid = True
        if not valid:
            raise InputError('Request contains improper data types for key {}.'.format(key))

    # ensures strings are not empty unless specified
    for key in validation.keys():
        if 'str' in validation[key] and not ("" in validation[key] or 'NoneType' in validation[key]):
            if "".join(e for e in data[key] if e.isalnum() or e in ['<', '>', '=']) == '':
                raise InputError('Request cannot contain empty or only non-alphanumeric string for columns.')

#===============================================================================
# Sends an email to the user with given inputs
def send_mail(user_email, subject, content):
    try:
        to_email = sendgrid.helpers.mail.To(email=user_email)
        from_email = sendgrid.helpers.mail.Email(email=current_app.config['OUTBOUND_EMAIL'])
        subject = '[ARRT] ' + subject
        content = sendgrid.helpers.mail.Content(
            'text/html',
            '''<html><body>
                ''' + str(content) + '''
            </body></html>'''
        )

        sg = sendgrid.SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        mail = sendgrid.helpers.mail.Mail(from_email, to_email, subject, content)
        response_mail = sg.client.mail.send.post(request_body=mail.get())
        if not re.search('^2(00|02)$', str(response_mail.status_code)):
            raise Exception('ERROR ' + str(response_mail.status_code))
        return True
    except Exception as e:
        raise Exception(e)
