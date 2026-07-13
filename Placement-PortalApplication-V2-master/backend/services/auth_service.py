from models.user import db, User
from models.student import Student
from models.company import Company
from utils.jwt_utils import generate_token
from utils.validators import validate_student_registration, validate_company_registration

def register_student(data):
    errors = validate_student_registration(data)
    if errors:
        return None, errors

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return None, ['Email already registered']

    user = User(
        email=data['email'],
        role='student'
    )
    user.set_password(data['password'])

    student = Student(
        name=data['name'],
        branch=data['branch'],
        cgpa=float(data['cgpa']),
        graduation_year=int(data['graduation_year']),
        resume_path=data.get('resume_path')
    )
    student.user = user

    try:
        db.session.add(user)
        db.session.add(student)
        db.session.commit()

        token = generate_token(user.id, user.role)
        return {
            'token': token,
            'user': user.to_dict(),
            'student': student.to_dict()
        }, None

    except Exception as e:
        db.session.rollback()
        return None, [f'Registration failed: {str(e)}']

def register_company(data):
    errors = validate_company_registration(data)
    if errors:
        return None, errors

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return None, ['Email already registered']

    user = User(
        email=data['email'],
        role='company'
    )
    user.set_password(data['password'])

    company = Company(
        company_name=data['company_name'],
        hr_contact=data.get('hr_contact'),
        website=data.get('website'),
        approval_status='pending'
    )
    company.user = user

    try:
        db.session.add(user)
        db.session.add(company)
        db.session.commit()

        token = generate_token(user.id, user.role)
        return {
            'token': token,
            'user': user.to_dict(),
            'company': company.to_dict()
        }, None

    except Exception as e:
        db.session.rollback()
        return None, [f'Registration failed: {str(e)}']

def login_user(email, password):
    if not email or not password:
        return None, 'Email and password are required'

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return None, 'Invalid email or password'

    if not user.is_active:
        return None, 'Account is not active'

    token = generate_token(user.id, user.role)

    result = {
        'token': token,
        'user': user.to_dict()
    }

    if user.role == 'student' and user.student:
        result['student'] = user.student.to_dict()
    elif user.role == 'company' and user.company:
        result['company'] = user.company.to_dict()

    return result, None
