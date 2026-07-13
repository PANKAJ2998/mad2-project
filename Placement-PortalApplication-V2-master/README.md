# 🎓 Placement Portal Application

A comprehensive full-stack web application for managing campus placement drives, connecting students, companies, and administrators in a seamless placement management system.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

The Placement Portal Application is a robust platform designed to streamline the campus recruitment process. It facilitates interaction between three key user roles:

- **Admin**: Manages companies, drives, and oversees the entire placement process
- **Company**: Creates and manages placement drives, reviews applications
- **Student**: Browses available drives, applies for positions, tracks application status

## ✨ Features

### Admin Dashboard
- 📊 Real-time analytics with interactive charts (Chart.js)
- 👥 Company management (approve/reject registrations)
- 🚀 Placement drive management and approval
- 📈 Application statistics and reporting
- 🎯 System-wide monitoring and control

### Company Portal
- 🏢 Company profile management
- 📝 Create and manage placement drives
- 📋 View and filter student applications
- ✅ Update application status (selected/rejected)
- 📊 Drive-specific analytics

### Student Portal
- 👤 Comprehensive student profile management
- 🔍 Browse available placement drives
- 📤 Apply to drives with one-click
- 📊 Track application status in real-time
- 🎯 Personalized dashboard

### General Features
- 🔐 Secure JWT-based authentication
- 🎨 Modern, responsive UI with Bootstrap 5
- ⚡ Fast caching with Redis
- 🔄 Background job processing with Celery
- 📱 PWA support for mobile devices
- 🌙 Clean and intuitive user interface
- ♿ Accessibility-focused design

## 🛠️ Tech Stack

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **State Management**: Pinia
- **Routing**: Vue Router 5
- **UI Framework**: Bootstrap 5 + Bootstrap Icons
- **Charts**: Chart.js 4.4
- **HTTP Client**: Axios
- **Build Tool**: Vite 7
- **PWA**: Service Workers + Manifest

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLite (with SQLAlchemy ORM)
- **Caching**: Redis 5.0
- **Task Queue**: Celery 5.3
- **Authentication**: JWT (PyJWT)
- **CORS**: Flask-CORS
- **Validation**: Marshmallow
- **Environment**: python-dotenv

## 🏗️ Architecture

```
placement-portal/
│
├── frontend/                  # Vue.js 3 Application
│   ├── public/               # Static assets & PWA files
│   ├── src/
│   │   ├── components/       # Reusable Vue components
│   │   ├── layouts/          # Layout components
│   │   ├── views/            # Page components
│   │   │   ├── admin/        # Admin-specific views
│   │   │   ├── company/      # Company-specific views
│   │   │   └── student/      # Student-specific views
│   │   ├── services/         # API service layer
│   │   ├── stores/           # Pinia state stores
│   │   └── router/           # Vue Router configuration
│   └── package.json
│
├── backend/                   # Flask API Server
│   ├── models/               # SQLAlchemy database models
│   ├── routes/               # API route handlers
│   ├── services/             # Business logic layer
│   ├── utils/                # Utility functions
│   ├── jobs/                 # Celery background tasks
│   ├── cache/                # Redis client configuration
│   ├── instance/             # SQLite database location
│   ├── app.py                # Flask application entry point
│   ├── config.py             # Configuration settings
│   └── requirements.txt      # Python dependencies
│
└── README.md                 # This file
```

## 🚀 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 20.19.0 or higher
- **Redis**: Latest stable version
- **Git**: Latest version

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd placement_portal_application_23f2001882
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file in backend directory
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start Redis server**
   ```bash
   # Windows (using Redis installer)
   redis-server

   # Linux
   sudo service redis-server start

   # Mac
   brew services start redis
   ```

6. **Run the Flask application**
   ```bash
   python app.py
   ```
   Backend will be available at `http://localhost:5000`

7. **Start Celery worker (Optional - for background jobs)**
   ```bash
   # In a new terminal, from backend directory
   celery -A jobs.celery_worker.celery worker --loglevel=info
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

4. **Build for production**
   ```bash
   npm run build
   ```

## ⚙️ Configuration

### Backend Configuration (.env)

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Admin Credentials
ADMIN_EMAIL=admin@placement.edu
ADMIN_PASSWORD=admin123
```

### Frontend Configuration

API endpoint is configured in `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000'
```

## 📖 Usage

### Default Admin Login

```
Email: admin@placement.edu
Password: admin123
```

### User Registration Flow

1. **Student Registration**
   - Navigate to `/register/student`
   - Fill in student details (name, roll number, email, etc.)
   - Account is created and active immediately

2. **Company Registration**
   - Navigate to `/register/company`
   - Fill in company details
   - Wait for admin approval before accessing portal

### Creating a Placement Drive (Company)

1. Login as company
2. Navigate to "Create Drive"
3. Fill in drive details (role, package, eligibility, etc.)
4. Submit for admin approval
5. Once approved, students can view and apply

### Applying to Drives (Student)

1. Login as student
2. Navigate to "Browse Drives"
3. View available drives
4. Click "Apply" on desired drives
5. Track status in "My Applications"

## 📚 API Documentation

### Authentication Endpoints

```
POST   /auth/login              # User login
POST   /auth/register/student   # Student registration
POST   /auth/register/company   # Company registration
```

### Admin Endpoints

```
GET    /admin/dashboard         # Dashboard analytics
GET    /admin/companies         # List all companies
POST   /admin/approve-company/:id    # Approve company
POST   /admin/reject-company/:id     # Reject company
GET    /admin/drives            # List all drives
POST   /admin/approve-drive/:id      # Approve drive
PUT    /admin/drive/:id         # Update drive
DELETE /admin/drive/:id         # Delete drive
```

### Company Endpoints

```
GET    /company/dashboard       # Company dashboard
GET    /company/profile         # Get company profile
PUT    /company/profile         # Update company profile
POST   /company/create-drive    # Create new drive
GET    /company/my-drives       # List company's drives
GET    /company/drive-applications/:id   # Get drive applications
POST   /company/update-application-status # Update application status
```

### Student Endpoints

```
GET    /student/dashboard       # Student dashboard
GET    /student/profile         # Get student profile
PUT    /student/profile         # Update student profile
GET    /student/drives          # Browse available drives
POST   /student/apply-drive/:id # Apply to drive
GET    /student/my-applications # Get student's applications
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Follow Vue.js 3 style guide
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Student ID**: 23f2001882
- **Institution**: IIT Madras BS Degree Programme

## 🙏 Acknowledgments

- IIT Madras BS Degree Programme
- Vue.js and Flask communities
- All contributors and testers

## 📧 Support

For support, email your instructor or raise an issue in the repository.

---

**⭐ Star this repository if you find it helpful!**

## 🗺️ Roadmap

- [ ] Email notifications for application updates
- [ ] Advanced search and filtering
- [ ] Export reports as PDF/Excel
- [ ] Mobile application (React Native)
- [ ] Video interview scheduling
- [ ] Resume parsing and matching
- [ ] Multi-language support
- [ ] Dark mode theme

## 📸 Screenshots

<!-- Add screenshots here -->

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin-dashboard.png)

### Student Portal
![Student Portal](docs/screenshots/student-portal.png)

### Company Portal
![Company Portal](docs/screenshots/company-portal.png)

---

Made with ❤️ for campus placements
