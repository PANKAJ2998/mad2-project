from flask import Blueprint, request
from services.drive_service import create_drive, get_company_drives, update_drive, delete_drive
from services.application_service import get_drive_applications, update_application_status
from utils.jwt_utils import token_required, role_required
from utils.response import success_response, error_response

company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/create-drive', methods=['POST'])
@token_required
@role_required('company')
def create_drive_route():
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    user_id = request.current_user['user_id']
    result, errors = create_drive(user_id, data)

    if errors:
        return error_response('Failed to create drive', errors=errors, status=400)

    return success_response('Drive created successfully', data=result, status=201)

@company_bp.route('/my-drives', methods=['GET'])
@token_required
@role_required('company')
def get_my_drives():
    user_id = request.current_user['user_id']
    drives, error = get_company_drives(user_id)

    if error:
        return error_response(error, status=404)

    return success_response('Drives retrieved successfully', data=drives)

@company_bp.route('/drive/<int:drive_id>', methods=['PUT'])
@token_required
@role_required('company')
def update_drive_route(drive_id):
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    user_id = request.current_user['user_id']
    result, error = update_drive(user_id, drive_id, data, is_admin=False)

    if error:
        return error_response(error, status=400)

    return success_response('Drive updated successfully', data=result)

@company_bp.route('/drive/<int:drive_id>', methods=['DELETE'])
@token_required
@role_required('company')
def delete_drive_route(drive_id):
    user_id = request.current_user['user_id']
    result, error = delete_drive(user_id, drive_id, is_admin=False)

    if error:
        return error_response(error, status=400)

    return success_response('Drive deleted successfully', data=result)

@company_bp.route('/drive-applications/<int:drive_id>', methods=['GET'])
@token_required
@role_required('company')
def get_applications_for_drive(drive_id):
    user_id = request.current_user['user_id']
    applications, error = get_drive_applications(user_id, drive_id)

    if error:
        return error_response(error, status=403)

    return success_response('Applications retrieved successfully', data=applications)

@company_bp.route('/update-application-status', methods=['POST'])
@token_required
@role_required('company')
def update_status():
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    application_id = data.get('application_id')
    new_status = data.get('status')

    if not application_id or not new_status:
        return error_response('application_id and status are required', status=400)

    user_id = request.current_user['user_id']
    result, error = update_application_status(user_id, application_id, new_status)

    if error:
        return error_response(error, status=400)

    return success_response('Application status updated', data=result)
