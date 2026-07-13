from models.user import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    resume_path = db.Column(db.String(255))

    applications = db.relationship('Application', backref='student', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'branch': self.branch,
            'cgpa': self.cgpa,
            'graduation_year': self.graduation_year,
            'resume_path': self.resume_path
        }

    def meets_eligibility(self, drive):
        if self.cgpa < drive.eligibility_cgpa:
            return False
        if drive.eligibility_branch and self.branch not in drive.eligibility_branch.split(','):
            return False
        if drive.eligibility_year and self.graduation_year != drive.eligibility_year:
            return False
        return True
