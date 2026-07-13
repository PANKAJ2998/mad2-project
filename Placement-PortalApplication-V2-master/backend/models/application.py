from models.user import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied')

    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)

    def to_dict(self, include_drive=False, include_student=False):
        data = {
            'id': self.id,
            'student_id': self.student_id,
            'drive_id': self.drive_id,
            'application_date': self.application_date.isoformat(),
            'status': self.status
        }
        if include_drive:
            data['drive'] = self.drive.to_dict(include_company=True)
        if include_student:
            data['student'] = self.student.to_dict()
        return data
