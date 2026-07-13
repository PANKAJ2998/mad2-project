from flask import Blueprint, request
from services.drive_service import get_student_drives
from services.application_service import apply_to_drive, get_student_applications
from services.student_service import update_student_profile, get_student_profile
from utils.jwt_utils import token_required, role_required
from utils.response import success_response, error_response

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/profile', methods=['GET'])
@token_required
@role_required('student')
def get_profile():
    user_id = request.current_user['user_id']
    profile, error = get_student_profile(user_id)

    if error:
        return error_response(error, status=404)

    return success_response('Profile retrieved successfully', data=profile)

@student_bp.route('/profile', methods=['PUT'])
@token_required
@role_required('student')
def update_profile():
    user_id = request.current_user['user_id']
    data = request.get_json()

    result, error = update_student_profile(user_id, data)

    if error:
        return error_response(error, status=400)

    return success_response('Profile updated successfully', data=result)

@student_bp.route('/drives', methods=['GET'])
@token_required
@role_required('student')
def get_drives():
    user_id = request.current_user['user_id']
    drives, error = get_student_drives(user_id)

    if error:
        return error_response(error, status=404)

    return success_response('Available drives retrieved', data=drives)

@student_bp.route('/apply-drive/<int:drive_id>', methods=['POST'])
@token_required
@role_required('student')
def apply_drive(drive_id):
    user_id = request.current_user['user_id']
    result, error = apply_to_drive(user_id, drive_id)

    if error:
        return error_response(error, status=400)

    return success_response('Applied to drive successfully', data=result, status=201)

@student_bp.route('/my-applications', methods=['GET'])
@token_required
@role_required('student')
def get_my_applications():
    user_id = request.current_user['user_id']
    applications, error = get_student_applications(user_id)

    if error:
        return error_response(error, status=404)

    return success_response('Applications retrieved successfully', data=applications)
