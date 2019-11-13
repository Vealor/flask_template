# ~~~ Utils:
import datetime
import os
import re
import sendgrid
import zipfile
import shutil
from anytree import Node, RenderTree
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
    if not isinstance(data, dict):
        raise ValueError('Input payload for endpoint must be a dictionary.')
    # Ensures keys in validation are all in data. Data can have excess keys.
    missing_vars = [x for x in validation.keys() if not x in data.keys()]
    if missing_vars:
        raise ValueError('Request is missing required keys: {}'.format(missing_vars))

    # Esures that the datatypes specified in validation match the types in data.
    # Example Available types:
    #   int, float, bool, str, list, tuple, dict, class, object, '', NoneType
    for key in validation.keys():
        valid = False
        for datatype in validation[key]:
            if datatype == 'NoneType':
                if isinstance(data[key],(str, type(None))):
                    valid = True
            elif datatype == '':
                if data[key] == '':
                    valid = True
            elif isinstance(data[key], eval(datatype)):
                valid = True
        if not valid:
            raise ValueError('Request contains improper data types for key {}.'.format(key))

    # ensures strings are not empty unless specified
    for key in validation.keys():
        if 'str' in validation[key] and not ("" in validation[key] or 'NoneType' in validation[key]):
            if "".join(e for e in data[key] if e.isalnum() or e in ['<','>','=']) == '':
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
# Unzips all SAP source data text files from a nested zip file.
def source_data_unzipper(data, response):

    # def extract_nested_zip(zippedFile, toFolder, outputPath):
    #     try:
    #         with zipfile.ZipFile(zippedFile, 'r') as zfile:
    #             zfile.extractall(path=outputPath)
    #             print('Extracted file to' + str(outputPath))
    #         print('Removing file' + str(zippedFile))
    #         os.remove(zippedFile)
    #         print('walking to' + toFolder)
    #         for root, dirs, files in os.walk(toFolder):
    #             print(root, dirs, files)
    #             for filename in files:
    #                 print(filename)
    #                 if re.search(r'\.(?i)ZIP$', filename):
    #                     fileSpec = os.path.join(root, filename)
    #                     print('Accessing ' + str(fileSpec))
    #                     extract_nested_zip(fileSpec, root, outputPath)
    #     except NotImplementedError:
    #         raise Exception(str(zippedFile) + ' has compression errors. Please fix')

    def extract_nested_zip(currentfolder, outputfolder):
        try:
            for root, dirs, files in os.walk(currentfolder):
                for filename in files:
                    if re.search(r'\.(?i)ZIP$', filename):
                        with zipfile.ZipFile(os.path.join(root, filename), 'r') as zfile:
                            zfile.extractall(path=outputfolder)
                        os.remove(os.path.join(root, filename))
                        #extract_nested_zip(root, output_folder)
                        # os.rename(os.path.join(root, filename), os.path.join(outputPath, filename))
                if dirs:
                    for dir in dirs:
                        extract_nested_zip(dir, outputfolder)

        except OSError as e:
            raise Exception(str(e))

    def move_nested_folder(currentfolder, outputPath):
        try:
            for root, dirs, files in os.walk(currentfolder):
                for filename in files:
                    if re.search(r'\.(?i)TXT$', filename):
                        os.rename(os.path.join(root, filename), os.path.join(outputPath, filename))
                for dir in dirs:
                    move_nested_folder(dir, outputPath)
        except OSError as e:
            raise Exception(str(e))

    def remove_empty_folders(inPath):
        try:
            for root, dirs, files in os.walk(inPath):
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))
        except OSError as e:
            raise Exception(e)

    if os.environ['FLASK_ENV'] == 'development':
        current_input_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'],  str(data['project_id']), current_app.config['CAPS_RAW_LOCATION'])
        current_output_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
        if data['file_name'].lower().endswith('.zip'):
            extract_nested_zip(current_input_path, current_output_path)
            while (True in [file.lower().endswith('.zip') for file in os.listdir(current_output_path)]):
                extract_nested_zip(current_output_path, current_output_path)
            print('out of while loop')
            move_nested_folder(current_output_path, current_output_path)
            #remove_empty_folders(current_output_path)
        else:
            raise Exception('Filename ' + str(data['file_name']) + ' does not end with .zip')
    elif os.environ['FLASK_ENV'] == 'production':
        #use blob storage
        pass
    else:
        raise Exception('Environ not present. Choose development or production')
    return response


#===============================================================================
# Unzips all SAP source data text files from a nested zip file.

def project_path_create(data, response):
    if os.environ['FLASK_ENV'] == 'development':
        if not os.path.exists(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']))):
            print('path does not exist, creating project')
            os.mkdir(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id'])))
            folders = ['sap_data', 'caps_gen_unzipped', 'caps_gen_raw', 'caps_gen_master']
            for folder in folders:
                os.mkdir((os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), folder)))
        else:
            response['message'] = 'Proceeding: Path {} has already been created for this project'.format(str(data['project_id']))
            return response
    elif os.environ['FLASK_ENV'] == 'testing':
        if not os.path.exists(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']))):
            print('path does not exist, creating project')
            os.mkdir(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id'])))
            folders = ['sap_data', 'caps_gen_unzipped', 'caps_gen_raw', 'caps_gen_master']
            for folder in folders:
                os.mkdir((os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), folder)))
        else:
            response['message'] = 'Proceeding: Path {} has already been created for this project'.format(str(data['project_id']))
            return response

        # project_dirs = current_app.config['FILE_SERVICE'].list_directories_and_files('caps-gen-processing')
        # project_dirs = [int(dir.name) for dir in current_app.config['FILE_SERVICE'].list_directories_and_files('caps-gen-processing')]
        #
        # if data['project_id'] not in project_dirs:
        #     current_app.config['FILE_SERVICE'].create_directory(fail_on_exist = True, share_name=current_app.config['CAPS_BASE_DIR'],
        #                                                         directory_name='{project_id}'.format(project_id = data['project_id']))
        #     current_app.config['FILE_SERVICE'].create_directory(fail_on_exist = True, share_name=current_app.config['CAPS_BASE_DIR'],
        #                                                         directory_name='{project_id}/{CAPS_RAW_LOCATION}'.format(project_id = data['project_id'], CAPS_RAW_LOCATION = current_app.config['CAPS_RAW_LOCATION']))
        #     current_app.config['FILE_SERVICE'].create_directory(fail_on_exist = True, share_name=current_app.config['CAPS_BASE_DIR'],
        #                                                         directory_name='{project_id}/{CAPS_UNZIPPING_LOCATION}'.format(project_id = data['project_id'], CAPS_UNZIPPING_LOCATION = current_app.config['CAPS_UNZIPPING_LOCATION']))
        #     current_app.config['FILE_SERVICE'].create_directory(fail_on_exist = True, share_name=current_app.config['CAPS_BASE_DIR'],
        #                                                         directory_name='{project_id}/{CAPS_MASTER_LOCATION}'.format(project_id = data['project_id'], CAPS_MASTER_LOCATION = current_app.config['CAPS_MASTER_LOCATION']))
        # else:
        #     response['message'] = 'Path {} has been created for this project'.format(str(data['project_id']))
        #     return response
    else:
        raise ValueError('Environ not present. Choose development or testing')
    return response

#===============================================================================
# Map datatype to regex for data quality check
def map_regex(dt_type):
    regex = ''
    if dt_type == 'dt_varchar':
        regex = '.*'
    elif dt_type == 'dt_float':
        regex = '^(?:\-)?\d*\.{1}\d+$'
    elif dt_type == 'dt_int':
        regex = '^(?:\-)?\d+$'
    elif dt_type == 'dt_date':
        regex = '^(0[1-9]|1[012])\/(0[1-9]|[1-2][0-9]|3[01])\/\d{4}$'
    else:
        raise Exception('No regex implmented for the given data type: {}'.format(dt_type))
    return regex

#===============================================================================
# Recursion helper for data quality check
def recursive_insert(root : Node, sub_str):
    char = sub_str[0]
    flag = False
    if root.children:
        for child in root.children:
            if char == child.name:
                if len(sub_str) > 1:
                    recursive_insert(child, sub_str[1:])
                else:
                    child.count += 1
                flag = True
    elif not flag:
        new_node = Node(char, parent=root, count=0)
        if len(sub_str) > 1:
            recursive_insert(new_node, sub_str[1:])
        else:
            new_node.count += 1

def recursive_find(root : Node, sub_str):
    char = sub_str[0]
    if root.children:
        for child in root.children:
            if char == child.name:
                if len(sub_str) > 1:
                    return recursive_find(child, sub_str[1:])
                else:
                    if child.count > 0:
                        return True
    return False
