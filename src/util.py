# ~~~ Utils:
import datetime
import os
import re
import sendgrid
import zipfile
from flask import current_app

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
    if isinstance(data, list):
        # Ensures keys in validation are all in data. Data can have excess keys.
        if [x for x in validation.keys() if not x in data.keys()]:
            raise ValueError('Request is missing required keys.')

        # Esures that the datatypes specified in validation match the types in data.
        # Example Available types:
        #   int, float, bool, str, list, tuple, dict, class, object
        if [x for x in validation.keys() if not isinstance(data[x], eval(validation[x]))]:
            raise ValueError('Request contains improper data types for keys.')

        # ensures strings are not empty
        for x in validation.keys():
            if validation[x] == 'str':
                if "".join(e for e in data[x] if e.isalnum()) == '':
                    raise ValueError('Request cannot contain empty or only non-alphanumeric string for columns.')
    elif isinstance(data, dict):
        # Ensures keys in validation are all in data. Data can have excess keys.
        if {x for x in validation.keys() if not x in data.keys()}:
            raise ValueError('Request is missing required keys.')

        # Esures that the datatypes specified in validation match the types in data.
        # Example Available types:
        #   int, float, bool, str, list, tuple, dict, class, object
        if {x for x in validation.keys() if not isinstance(data[x], eval(validation[x]))}:
            raise ValueError('Request contains improper data types for keys.')

        # ensures strings are not empty
        for x in validation.keys():
            if validation[x] == 'str':
                if "".join(e for e in data[x] if e.isalnum()) == '':
                    raise ValueError('Request cannot contain empty or only non-alphanumeric string for columns.')


#===============================================================================
# Sends an email to the user with given inputs
def send_mail(user_email, subject, content):
    try:
        to_email = sendgrid.helpers.mail.To(email=user_email)
        from_email = sendgrid.helpers.mail.Email(email=current_app.config['OUTBOUND_EMAIL'])
        subject = '[ARRT] '+ subject
        content = sendgrid.helpers.mail.Content(
            'text/html',
            '''<html><body>
                '''+str(content)+'''
            </body></html>'''
        )

        sg = sendgrid.SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        mail = sendgrid.helpers.mail.Mail(from_email, to_email, subject, content)
        response_mail = sg.client.mail.send.post(request_body=mail.get())
        if not re.search('^2(00|02)$', str(response_mail.status_code)):
            raise 'ERROR '+str(response_mail.status_code)
        return True
    except Exception as e:
        raise e

#===============================================================================



#===============================================================================
# Sends an email to the user with given inputs
def get_data(data, response):
    def extract_nested_zip(zippedFile, toFolder):
        try:
            with zipfile.ZipFile(zippedFile, 'r') as zfile:
                zfile.extractall(path=toFolder)
            os.remove(zippedFile)
            for root, dirs, files in os.walk(toFolder):
                for filename in files:
                    if re.search(r'\.(?i)ZIP$', filename):
                        fileSpec = os.path.join(root, filename)
                        extract_nested_zip(fileSpec, root)
        except NotImplementedError:
            raise Exception(str(zippedFile) + ' has compression errors. Please fix')
        except Exception as e:
            raise Exception(str(e))
    if os.environ['FLASK_ENV'] == 'development':
        current_input_path = os.path.join(os.getcwd(), str(data['project_id']), current_app.config['CAPS_RAW_LOCATION'])
        current_output_path = os.path.join(os.getcwd(), str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
        cwd = os.getcwd()
        os.chdir(current_input_path)

        if data['file_name'].lower().endswith('.zip'):
            try:
                extract_nested_zip(os.path.join(current_input_path, data['file_name']), current_output_path)
            except Exception as e:
                raise Exception(str(e))
        else:
            raise Exception(str(data['file_name']) + 'does not end with .zip')
        os.chdir(cwd)
    elif os.environ['FLASK_ENV'] == 'production':
        #use blob storage
        pass
    else:
        raise Exception('Environ not present. Choose development or production')
    return response


