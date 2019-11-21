import os
import re
import zipfile
import shutil
from flask import current_app

#===============================================================================
# Unzips all SAP source data text files from a nested zip file.
def source_data_unzipper(data, response):

    def pull_out_of_folder(outdir, folder):
        for file in os.listdir(os.path.join(outdir, folder)):
            shutil.move(os.path.join(outdir, folder, file), os.path.join(outdir, folder, '..', file))
        os.rmdir(os.path.join(outdir, folder))
        return

    def unzip_file(outdir, zipper):
        with zipfile.ZipFile(os.path.join(outdir, zipper), 'r') as zipObj:
            zipObj.extractall(outdir)
        os.remove(os.path.join(outdir, zipper))
        return

    if os.environ['FLASK_ENV'] == 'development' or os.environ['FLASK_ENV'] == 'testing':
        indir = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'],  str(data['project_id']), current_app.config['CAPS_RAW_LOCATION'])
        outdir = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])

        if data['file_name'].lower().endswith('.zip'):
            queue = [i for i in os.listdir(os.path.join(indir)) if os.path.isfile(os.path.join(indir,i)) and re.match('.*\.[zZ][iI][pP]$',i)]
            for file in queue:
                shutil.copyfile(os.path.join(indir,file), os.path.join(outdir,file))
            print(queue)
            type = 'zip'
            while len(queue) > 0:
                print(queue)
                print(type)
                if type == 'folder':
                    for folder in queue:
                        pull_out_of_folder(outdir,folder)
                if type == 'zip':
                    for zip in queue:
                        unzip_file(outdir,zip)
                folders = [f for f in os.listdir(outdir) if os.path.isdir(os.path.join(outdir,f))]
                zips = [i for i in os.listdir(outdir) if os.path.isfile(os.path.join(outdir,i)) and re.match('.*\.[zZ][iI][pP]$',i)]
                if folders:
                    type = 'folder'
                    queue = folders
                elif zips:
                    type = 'zip'
                    queue = zips
                else:
                    queue = []

            os.remove(os.path.join(indir,file))
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
        raise Exception('Environment not specified or not present. Choose development or testing')
    return response
