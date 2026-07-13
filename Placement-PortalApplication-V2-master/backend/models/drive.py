from models.user import db
from datetime import datetime

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    eligibility_branch = db.Column(db.String(255))
    eligibility_cgpa = db.Column(db.Float, default=0.0)
    eligibility_year = db.Column(db.Integer)
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='drive', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_company=False):
        data = {
            'id': self.id,
            'company_id': self.company_id,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'eligibility_branch': self.eligibility_branch,
            'eligibility_cgpa': self.eligibility_cgpa,
            'eligibility_year': self.eligibility_year,
            'deadline': self.deadline.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
        if include_company:
            data['company_name'] = self.company.company_name
        return data

    def is_active(self):
        return self.status == 'approved' and self.deadline > datetime.utcnow()
