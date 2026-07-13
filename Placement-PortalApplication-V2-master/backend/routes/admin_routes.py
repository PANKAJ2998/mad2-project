from flask import Blueprint, request
from models.user import db
from models.company import Company
from models.drive import PlacementDrive
from models.application import Application
from services.drive_service import approve_drive, get_all_drives, update_drive, delete_drive
from utils.jwt_utils import token_required, role_required
from utils.response import success_response, error_response
from cache.redis_client import redis_client

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('admin')
def get_dashboard():
    cache_key = 'admin:dashboard'
    cached = redis_client.get(cache_key)
    if cached:
        return success_response('Dashboard data retrieved', data=cached)

    total_companies = Company.query.count()
    pending_companies = Company.query.filter_by(approval_status='pending').count()
    approved_companies = Company.query.filter_by(approval_status='approved').count()

    total_drives = PlacementDrive.query.count()
    pending_drives = PlacementDrive.query.filter_by(status='pending').count()
    approved_drives = PlacementDrive.query.filter_by(status='approved').count()

    total_applications = Application.query.count()
    selected_applications = Application.query.filter_by(status='selected').count()

    dashboard_data = {
        'companies': {
            'total': total_companies,
            'pending': pending_companies,
            'approved': approved_companies
        },
        'drives': {
            'total': total_drives,
            'pending': pending_drives,
            'approved': approved_drives
        },
        'applications': {
            'total': total_applications,
            'selected': selected_applications
        }
    }

    redis_client.set(cache_key, dashboard_data)
    return success_response('Dashboard data retrieved', data=dashboard_data)

@admin_bp.route('/companies', methods=['GET'])
@token_required
@role_required('admin')
def get_companies():
    companies = Company.query.all()
    return success_response('Companies retrieved', data=[c.to_dict() for c in companies])

@admin_bp.route('/approve-company/<int:company_id>', methods=['POST'])
@token_required
@role_required('admin')
def approve_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return error_response('Company not found', status=404)

    company.approval_status = 'approved'
    try:
        db.session.commit()
        redis_client.clear_pattern('admin:*')
        return success_response('Company approved successfully', data=company.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to approve company: {str(e)}', status=500)

@admin_bp.route('/reject-company/<int:company_id>', methods=['POST'])
@token_required
@role_required('admin')
def reject_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return error_response('Company not found', status=404)

    company.approval_status = 'rejected'
    try:
        db.session.commit()
        redis_client.clear_pattern('admin:*')
        return success_response('Company rejected', data=company.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to reject company: {str(e)}', status=500)

@admin_bp.route('/drives', methods=['GET'])
@token_required
@role_required('admin')
def get_drives():
    drives = get_all_drives()
    return success_response('Drives retrieved', data=drives)

@admin_bp.route('/approve-drive/<int:drive_id>', methods=['POST'])
@token_required
@role_required('admin')
def approve_drive_route(drive_id):
    result, error = approve_drive(drive_id)
    if error:
        return error_response(error, status=400)

    redis_client.clear_pattern('admin:*')
    return success_response('Drive approved successfully', data=result)

@admin_bp.route('/drive/<int:drive_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_drive_route(drive_id):
    data = request.get_json()
    if not data:
        return error_response('No data provided', status=400)

    user_id = request.current_user['user_id']
    result, error = update_drive(user_id, drive_id, data, is_admin=True)

    if error:
        return error_response(error, status=400)

    redis_client.clear_pattern('admin:*')
    return success_response('Drive updated successfully', data=result)

@admin_bp.route('/drive/<int:drive_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_drive_route(drive_id):
    user_id = request.current_user['user_id']
    result, error = delete_drive(user_id, drive_id, is_admin=True)

    if error:
        return error_response(error, status=400)

    redis_client.clear_pattern('admin:*')
    return success_response('Drive deleted successfully', data=result)
