from models.user import db
from models.student import Student
from cache.redis_client import redis_client

def get_student_profile(user_id):
    """Get student profile by user_id"""
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return None, 'Student profile not found'

    return student.to_dict(), None

def update_student_profile(user_id, data):
    """Update student profile"""
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return None, 'Student profile not found'

    # Update allowed fields
    if 'branch' in data:
        student.branch = data['branch']

    if 'cgpa' in data:
        try:
            cgpa = float(data['cgpa'])
            if cgpa < 0 or cgpa > 10:
                return None, 'CGPA must be between 0 and 10'
            student.cgpa = cgpa
        except (ValueError, TypeError):
            return None, 'Invalid CGPA value'

    if 'graduation_year' in data:
        try:
            year = int(data['graduation_year'])
            if year < 2024 or year > 2030:
                return None, 'Graduation year must be between 2024 and 2030'
            student.graduation_year = year
        except (ValueError, TypeError):
            return None, 'Invalid graduation year'

    if 'resume_path' in data:
        student.resume_path = data['resume_path']

    try:
        db.session.commit()
        # Clear student drives cache as eligibility might have changed
        redis_client.clear_pattern(f'drives:student:{user_id}')
        return student.to_dict(), None
    except Exception as e:
        db.session.rollback()
        return None, f'Failed to update profile: {str(e)}'
