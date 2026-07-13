from jobs.celery_worker import celery
import csv
import os
from datetime import datetime

@celery.task(name='jobs.export_jobs.export_student_applications')
def export_student_applications(student_id):
    """
    Generate CSV file of student applications asynchronously.
    This is a placeholder implementation.
    """
    try:
        from models.application import Application

        applications = Application.query.filter_by(student_id=student_id).all()

        filename = f'student_{student_id}_applications_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join('exports', filename)

        os.makedirs('exports', exist_ok=True)

        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['Application ID', 'Drive ID', 'Job Title', 'Company', 'Application Date', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for app in applications:
                writer.writerow({
                    'Application ID': app.id,
                    'Drive ID': app.drive_id,
                    'Job Title': app.drive.job_title,
                    'Company': app.drive.company.company_name,
                    'Application Date': app.application_date.strftime('%Y-%m-%d'),
                    'Status': app.status
                })

        return {
            'status': 'success',
            'filename': filename,
            'filepath': filepath,
            'record_count': len(applications),
            'timestamp': datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

@celery.task(name='jobs.export_jobs.export_drive_applications')
def export_drive_applications(drive_id):
    """
    Generate CSV file of all applications for a specific drive.
    """
    try:
        from models.application import Application

        applications = Application.query.filter_by(drive_id=drive_id).all()

        filename = f'drive_{drive_id}_applications_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join('exports', filename)

        os.makedirs('exports', exist_ok=True)

        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['Application ID', 'Student Name', 'Branch', 'CGPA', 'Application Date', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for app in applications:
                writer.writerow({
                    'Application ID': app.id,
                    'Student Name': app.student.name,
                    'Branch': app.student.branch,
                    'CGPA': app.student.cgpa,
                    'Application Date': app.application_date.strftime('%Y-%m-%d'),
                    'Status': app.status
                })

        return {
            'status': 'success',
            'filename': filename,
            'filepath': filepath,
            'record_count': len(applications),
            'timestamp': datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
