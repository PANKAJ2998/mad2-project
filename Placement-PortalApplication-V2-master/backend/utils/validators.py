import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, None

def validate_cgpa(cgpa):
    try:
        cgpa_float = float(cgpa)
        if 0.0 <= cgpa_float <= 10.0:
            return True, None
        return False, "CGPA must be between 0 and 10"
    except ValueError:
        return False, "Invalid CGPA format"

def validate_student_registration(data):
    errors = []

    if not data.get('email'):
        errors.append('Email is required')
    elif not validate_email(data['email']):
        errors.append('Invalid email format')

    if not data.get('password'):
        errors.append('Password is required')
    else:
        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            errors.append(msg)

    if not data.get('name'):
        errors.append('Name is required')

    if not data.get('branch'):
        errors.append('Branch is required')

    if not data.get('cgpa'):
        errors.append('CGPA is required')
    else:
        is_valid, msg = validate_cgpa(data['cgpa'])
        if not is_valid:
            errors.append(msg)

    if not data.get('graduation_year'):
        errors.append('Graduation year is required')

    return errors

def validate_company_registration(data):
    errors = []

    if not data.get('email'):
        errors.append('Email is required')
    elif not validate_email(data['email']):
        errors.append('Invalid email format')

    if not data.get('password'):
        errors.append('Password is required')
    else:
        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            errors.append(msg)

    if not data.get('company_name'):
        errors.append('Company name is required')

    return errors

def validate_drive_creation(data):
    errors = []

    if not data.get('job_title'):
        errors.append('Job title is required')

    if not data.get('deadline'):
        errors.append('Deadline is required')

    if data.get('eligibility_cgpa'):
        is_valid, msg = validate_cgpa(data['eligibility_cgpa'])
        if not is_valid:
            errors.append(msg)

    return errors
