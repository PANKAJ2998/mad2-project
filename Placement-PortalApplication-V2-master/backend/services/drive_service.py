from models.user import db
from models.company import Company
from models.drive import PlacementDrive
from models.student import Student
from utils.validators import validate_drive_creation
from cache.redis_client import redis_client
from datetime import datetime

def create_drive(user_id, data):
    errors = validate_drive_creation(data)
    if errors:
        return None, errors

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return None, ['Company not found']

    if not company.is_approved():
        return None, ['Company must be approved to create drives']

    try:
        deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
    except Exception:
        return None, ['Invalid deadline format']

    drive = PlacementDrive(
        company_id=company.id,
        job_title=data['job_title'],
        job_description=data.get('job_description'),
        eligibility_branch=data.get('eligibility_branch'),
        eligibility_cgpa=float(data.get('eligibility_cgpa', 0.0)),
        eligibility_year=data.get('eligibility_year'),
        deadline=deadline,
        status='pending'
    )

    try:
        db.session.add(drive)
        db.session.commit()
        redis_client.clear_pattern('drives:*')
        return drive.to_dict(include_company=True), None
    except Exception as e:
        db.session.rollback()
        return None, [f'Failed to create drive: {str(e)}']

def get_company_drives(user_id):
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return None, 'Company not found'

    drives = PlacementDrive.query.filter_by(company_id=company.id).order_by(PlacementDrive.created_at.desc()).all()
    return [drive.to_dict() for drive in drives], None

def get_student_drives(user_id):
    cache_key = f'drives:student:{user_id}'
    cached = redis_client.get(cache_key)
    if cached:
        return cached, None

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return None, 'Student not found'

    drives = PlacementDrive.query.filter_by(status='approved').filter(
        PlacementDrive.deadline > datetime.utcnow()
    ).order_by(PlacementDrive.deadline.asc()).all()

    eligible_drives = [
        drive.to_dict(include_company=True)
        for drive in drives
        if student.meets_eligibility(drive)
    ]

    redis_client.set(cache_key, eligible_drives)
    return eligible_drives, None

def approve_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return None, 'Drive not found'

    drive.status = 'approved'
    try:
        db.session.commit()
        redis_client.clear_pattern('drives:*')
        return drive.to_dict(include_company=True), None
    except Exception as e:
        db.session.rollback()
        return None, f'Failed to approve drive: {str(e)}'

def get_all_drives():
    drives = PlacementDrive.query.order_by(PlacementDrive.created_at.desc()).all()
    return [drive.to_dict(include_company=True) for drive in drives]

def update_drive(user_id, drive_id, data, is_admin=False):
    """Update a drive. Companies can only update their own drives, admins can update any drive."""
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return None, 'Drive not found'

    # Check authorization
    if not is_admin:
        company = Company.query.filter_by(user_id=user_id).first()
        if not company or drive.company_id != company.id:
            return None, 'Unauthorized to update this drive'

    # Update fields
    if 'job_title' in data:
        drive.job_title = data['job_title']

    if 'job_description' in data:
        drive.job_description = data['job_description']

    if 'eligibility_branch' in data:
        drive.eligibility_branch = data['eligibility_branch']

    if 'eligibility_cgpa' in data:
        try:
            cgpa = float(data['eligibility_cgpa'])
            if cgpa < 0 or cgpa > 10:
                return None, 'CGPA must be between 0 and 10'
            drive.eligibility_cgpa = cgpa
        except (ValueError, TypeError):
            return None, 'Invalid CGPA value'

    if 'eligibility_year' in data:
        drive.eligibility_year = data['eligibility_year']

    if 'deadline' in data:
        try:
            deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
            drive.deadline = deadline
        except Exception:
            return None, 'Invalid deadline format'

    if 'status' in data and is_admin:
        drive.status = data['status']

    try:
        db.session.commit()
        redis_client.clear_pattern('drives:*')
        return drive.to_dict(include_company=True), None
    except Exception as e:
        db.session.rollback()
        return None, f'Failed to update drive: {str(e)}'

def delete_drive(user_id, drive_id, is_admin=False):
    """Delete a drive. Companies can only delete their own drives, admins can delete any drive."""
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return None, 'Drive not found'

    # Check authorization
    if not is_admin:
        company = Company.query.filter_by(user_id=user_id).first()
        if not company or drive.company_id != company.id:
            return None, 'Unauthorized to delete this drive'

    try:
        db.session.delete(drive)
        db.session.commit()
        redis_client.clear_pattern('drives:*')
        return {'id': drive_id, 'message': 'Drive deleted successfully'}, None
    except Exception as e:
        db.session.rollback()
        return None, f'Failed to delete drive: {str(e)}'
