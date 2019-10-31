'''
Tax Rate Endpoints
'''
from sqlalchemy import desc
from flask import Blueprint, jsonify
from src.models import Project, CapsGen, SapT007s

tax_rate = Blueprint('tax_rate', __name__)
#===============================================================================
# permission check
@tax_rate.route('/<int:project_id>', methods=['GET'])
def get_tax_rate_table(project_id):
    try:
        response = {'status': 'ok', 'message': '', 'payload': []}
        if Project.query.filter_by(id=project_id).count() < 1:
            raise ValueError('Project ID invalid.')
        # check if caps_gen exist, if exist proceed, if not send back error message
        capsgen = CapsGen.query.filter_by(project_id=project_id).order_by(desc(CapsGen.id)).first()
        if capsgen is not None:
            rows = SapT007s.query.filter_by(capsgen_id=capsgen.id).all()
            response['payload'] = [row.data for row in rows]
        else:
            raise ValueError("Caps has not been generated, Please generate caps first.")
    except ValueError as e:
        response = {'status': 'error', 'message': str(e), 'payload': []}
        return jsonify(response), 404
    except Exception as e:
        response = {'status': 'error', 'message': str(e), 'payload': []}
        return jsonify(response), 500
    return jsonify(response), 200
