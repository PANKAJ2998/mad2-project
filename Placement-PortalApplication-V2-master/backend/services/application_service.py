from models.user import db
from models.student import Student
from models.drive import PlacementDrive
from models.application import Application
from sqlalchemy.exc import IntegrityError

def apply_to_drive(user_id, drive_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return None, 'Student not found'

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return None, 'Drive not found'

    if not drive.is_active():
        return None, 'Drive is not active'

    if not student.meets_eligibility(drive):
        return None, 'Student does not meet eligibility criteria'

    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing_application:
        return None, 'Already applied to this drive'

    application = Application(
        student_id=student.id,
        drive_id=drive_id,
        status='applied'
    )

    try:
        db.session.add(application)
        db.session.commit()
        return application.to_dict(include_drive=True), None
    except IntegrityError:
        db.session.rollback()
        return None, 'Already applied to this drive'
    except Exception as e:
        db.session.rollback()
        return None, f'Failed to apply: {str(e)}'

def get_student_applications(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return None, 'Student not found'

    applications = Application.query.filter_by(student_id=student.id).order_by(
        Application.application_date.desc()
    ).all()

    return [app.to_dict(include_drive=True) for app in applications], None

def get_drive_applications(user_id, drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return None, 'Drive not found'

    if drive.company.user_id != user_id:
        return None, 'Unauthorized to view these applications'

    applications = Application.query.filter_by(drive_id=drive_id).order_by(
        Application.application_date.desc()
    ).all()

    return [app.to_dict(include_student=True) for app in applications], None

def update_application_status(user_id, application_id, new_status):
    application = Application.query.get(application_id)
    if not application:
        return None, 'Application not found'

    drive = application.drive
    if drive.company.user_id != user_id:
        return None, 'Unauthorized to update this application'

    valid_statuses = ['applied', 'shortlisted', 'selected', 'rejected']
    if new_status not in valid_statuses:
        return None, f'Invalid status. Must be one of: {", ".join(valid_statuses)}'

    application.status = new_status

    try:
        db.session.commit()
        return application.to_dict(include_student=True), None
    except Exception as e:
        db.session.rollback()
        return None, f'Failed to update status: {str(e)}'
