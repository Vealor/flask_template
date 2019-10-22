'''
General Endpoints
'''
from sqlalchemy import desc
from flask import Blueprint, jsonify
from src.models import Project, CapsGen, SapLfa1

client_vendor_master = Blueprint('client_vendor_master', __name__)
#===============================================================================
# General
@client_vendor_master.route('/<int:project_id>', methods=['GET'])
def get_client_vendor_master(project_id):
    try:
        code = 500
        response = {'status': 'ok', 'message': '', 'payload': []}
        if Project.query.filter_by(id=project_id).count() < 1:
            code = 404
            raise ValueError('Project ID invalid.')
        # check if caps_gen exist, if exist proceed, if not send back error message
        capsgen = CapsGen.query.filter_by(project_id=project_id).order_by(desc(CapsGen.id)).first()
        if capsgen is not None:
            # one capsgen should only accociate with one fa1 row
            # TODO: check with john I got multiple results here
            rows = SapLfa1.query.filter_by(capsgen_id=capsgen.id).all()
            client_vendor_data = [row.data for row in rows]
            response['payload'] = client_vendor_data
            code = 200
        else:
            code = 404
            raise ValueError("Caps has not been generated, Please generate caps first.")
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'error'
        response['payload'] = []
    return jsonify(response), code
