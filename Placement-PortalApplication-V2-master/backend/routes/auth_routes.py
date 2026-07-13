from flask import Blueprint, request
from services.auth_service import register_student, register_company, login_user
from utils.response import success_response, error_response

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/student', methods=['POST'])
def register_student_route():
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    result, errors = register_student(data)
    if errors:
        return error_response('Registration failed', errors=errors, status=400)

    return success_response('Student registered successfully', data=result, status=201)

@auth_bp.route('/register/company', methods=['POST'])
def register_company_route():
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    result, errors = register_company(data)
    if errors:
        return error_response('Registration failed', errors=errors, status=400)

    return success_response('Company registered successfully', data=result, status=201)

@auth_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    result, error = login_user(data.get('email'), data.get('password'))
    if error:
        return error_response(error, status=401)

    return success_response('Login successful', data=result)
