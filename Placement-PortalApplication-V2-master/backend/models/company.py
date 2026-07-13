from models.user import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default='pending')
    is_blacklisted = db.Column(db.Boolean, default=False)

    drives = db.relationship('PlacementDrive', backref='company', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'hr_contact': self.hr_contact,
            'website': self.website,
            'approval_status': self.approval_status,
            'is_blacklisted': self.is_blacklisted
        }

    def is_approved(self):
        return self.approval_status == 'approved' and not self.is_blacklisted
