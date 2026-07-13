# Placement Portal Application - Backend

A production-quality Flask backend for managing placement drives between students, companies, and institute admin.

## Tech Stack

- **Backend Framework**: Flask
- **Database**: SQLite (programmatically created)
- **Caching**: Redis
- **Background Jobs**: Celery + Redis
- **Authentication**: JWT
- **ORM**: SQLAlchemy
- **Validation**: Manual validation

## Project Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── models/                     # Database models
│   ├── user.py
│   ├── student.py
│   ├── company.py
│   ├── drive.py
│   └── application.py
│
├── routes/                     # API route handlers
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── company_routes.py
│   └── student_routes.py
│
├── services/                   # Business logic layer
│   ├── auth_service.py
│   ├── drive_service.py
│   └── application_service.py
│
├── utils/                      # Utility functions
│   ├── jwt_utils.py
│   ├── validators.py
│   └── response.py
│
├── jobs/                       # Celery background jobs
│   ├── celery_worker.py
│   ├── reminder_jobs.py
│   ├── report_jobs.py
│   └── export_jobs.py
│
└── cache/                      # Redis caching
    └── redis_client.py
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Redis server

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Ensure Redis is running:
```bash
redis-server
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```
The server will run on `http://localhost:5000`

2. Start the Celery worker (in a separate terminal):
```bash
celery -A jobs.celery_worker worker --loglevel=info
```

3. Start Celery Beat for scheduled tasks (optional, in another terminal):
```bash
celery -A jobs.celery_worker beat --loglevel=info
```

## Default Admin Credentials

- **Email**: admin@placement.edu
- **Password**: admin123

## API Endpoints

### Authentication

- `POST /auth/register/student` - Register a new student
- `POST /auth/register/company` - Register a new company
- `POST /auth/login` - Login

### Admin APIs

- `GET /admin/dashboard` - Get dashboard statistics
- `GET /admin/companies` - Get all companies
- `POST /admin/approve-company/<id>` - Approve a company
- `POST /admin/reject-company/<id>` - Reject a company
- `GET /admin/drives` - Get all drives
- `POST /admin/approve-drive/<id>` - Approve a drive

### Company APIs

- `POST /company/create-drive` - Create a new placement drive
- `GET /company/my-drives` - Get company's drives
- `GET /company/drive-applications/<drive_id>` - Get applications for a drive
- `POST /company/update-application-status` - Update application status

### Student APIs

- `GET /student/drives` - Get available drives (cached)
- `POST /student/apply-drive/<drive_id>` - Apply to a drive
- `GET /student/my-applications` - Get student's applications

## Business Rules

1. Admin is created automatically on first run
2. Companies must be approved by admin before creating drives
3. Drives must be approved by admin before students can see them
4. Students cannot apply twice to the same drive
5. Student eligibility is validated (CGPA, branch, graduation year)
6. Cache expires every 5 minutes

## Background Jobs

1. **Daily Reminders**: Send emails for upcoming application deadlines
2. **Monthly Reports**: Generate HTML report with placement statistics
3. **CSV Export**: Export student applications asynchronously

## Caching

Redis caching is implemented for:
- Student drive list (`drives:student:<user_id>`)
- Admin dashboard stats (`admin:dashboard`)

Cache TTL: 5 minutes

## Database Schema

### User
- id, email, password_hash, role, is_active, created_at

### Student
- id, user_id, name, branch, cgpa, graduation_year, resume_path

### Company
- id, user_id, company_name, hr_contact, website, approval_status, is_blacklisted

### PlacementDrive
- id, company_id, job_title, job_description, eligibility_branch, eligibility_cgpa, eligibility_year, deadline, status

### Application
- id, student_id, drive_id, application_date, status

## Development Notes

- Database file: `placement_portal.db` (auto-created)
- Code follows clean architecture principles
- Service layer handles business logic
- Routes remain thin
- Proper error handling throughout
- JWT tokens expire after 24 hours
