# 📚 Student Management System - Full-Stack Edition

**Version:** 2.0.0 | **Status:** ✅ Production Ready

A complete full-stack Student Management System built with **FastAPI** backend and **Jinja2** frontend, using **MySQL** database and **SQLAlchemy** ORM. This system manages students, courses, enrollment relationships, and attendance tracking with JWT-based admin authentication.

## ✨ Features

### 🌐 Web Interface
- ✅ **Responsive Web UI** - Mobile-friendly design with professional styling
- ✅ **Admin Dashboard** - Statistics and quick access to main features
- ✅ **Student Management UI** - Intuitive interface for CRUD operations
- ✅ **Form Validation** - Client-side validation with error handling
- ✅ **Navigation System** - Clean navbar with authentication-based menu

### 🔧 Core Features
- ✅ **Student Management** - CRUD operations for students
- ✅ **Course Management** - CRUD operations for courses
- ✅ **Student-Course Enrollment** - Many-to-many relationships with enroll/unenroll functionality
- ✅ **Attendance Tracking** - Mark attendance, generate reports, and track attendance by date/student
- ✅ **Admin Authentication** - JWT-based authentication with secure password hashing
- ✅ **Pagination Support** - Efficient data retrieval with configurable pagination
- ✅ **Database Migrations** - Alembic for version control of database schema
- ✅ **Comprehensive Logging** - Error and info logging throughout the application
- ✅ **RESTful APIs** - 20+ clean and intuitive API endpoints
- ✅ **Web Routes** - 8 template-based web page routes

## 🛠️ Tech Stack

### Frontend
- **Jinja2 3.1.2** - Server-side template engine
- **HTML5** - Semantic markup
- **CSS3** - Responsive styling
- **Vanilla JavaScript** - Client-side interactivity

### Backend
- **FastAPI 0.104.1** - Modern web framework for building APIs
- **SQLAlchemy 2.0.23** - ORM for database operations
- **MySQL 8.0+** - Relational database
- **Pydantic 2.5.0** - Data validation and serialization
- **python-jose 3.3.0** - JWT token handling
- **passlib[bcrypt] 1.7.4** - Secure password hashing
- **Alembic 1.12.1** - Database migrations
- **Uvicorn 0.24.0** - ASGI server

## 📁 Project Structure

```
Student Management System/
├── 📄 Documentation (NEW!)
│   ├── SETUP_AND_RUN.md ..................... Quick start guide
│   ├── WEB_UI_GUIDE.md ...................... UI documentation
│   ├── DEPLOYMENT_GUIDE.md .................. Production setup
│   ├── VALIDATION_CHECKLIST.md .............. Testing & validation
│   ├── COMPLETION_REPORT.md ................. Project summary
│   └── AI_COPILOT_INSTRUCTIONS_GUIDE.md .... Developer reference
│
├── 🌐 Web Frontend (NEW!)
│   ├── app/templates/ ....................... Jinja2 HTML templates
│   │   ├── layout.html ...................... Base template
│   │   ├── index.html ....................... Home page
│   │   ├── login.html ....................... Login page
│   │   ├── dashboard.html ................... Dashboard
│   │   ├── students.html .................... Students management
│   │   ├── add_student.html ................. Add student form
│   │   ├── edit_student.html ................ Edit student form
│   │   ├── courses.html ..................... Courses management
│   │   └── attendance.html .................. Attendance tracking
│   └── app/static/ .......................... Static assets
│       ├── css/style.css .................... Responsive styling (~700 lines)
│       ├── js/main.js ....................... Frontend utilities (~400 lines)
│       └── images/ .......................... Image assets
│
├── 🔌 Backend API
│   ├── app/core/
│   │   ├── config.py ........................ Pydantic Settings (environment variables)
│   │   ├── database.py ...................... SQLAlchemy engine, session, Base
│   │   └── security.py ...................... JWT and authentication dependencies
│   ├── app/models/
│   │   ├── admin.py ......................... Admin ORM model
│   │   ├── student.py ....................... Student model + student_course junction
│   │   ├── course.py ........................ Course model
│   │   └── attendance.py .................... Attendance model
│   ├── app/schemas/
│   │   ├── admin.py ......................... Admin Pydantic schemas
│   │   ├── student.py ....................... Student Pydantic schemas
│   │   ├── course.py ........................ Course Pydantic schemas
│   │   └── attendance.py .................... Attendance Pydantic schemas
│   ├── app/services/
│   │   ├── admin_service.py ................. Admin CRUD + authentication
│   │   ├── student_service.py ............... Student CRUD + enrollment
│   │   ├── course_service.py ................ Course CRUD
│   │   └── attendance_service.py ............ Attendance CRUD + reports
│   ├── app/routers/
│   │   ├── web_router.py .................... Web page routes (NEW!)
│   │   ├── auth_router.py ................... Authentication endpoints
│   │   ├── student_router.py ................ Student endpoints
│   │   ├── course_router.py ................. Course endpoints
│   │   └── attendance_router.py ............. Attendance endpoints
│   ├── app/utils/
│   │   ├── jwt_utils.py ..................... JWT token creation and validation
│   │   └── hashing.py ....................... Password hashing utilities
│   └── app/main.py .......................... FastAPI app initialization
│
├── 🗄️ Database
│   ├── alembic/ ............................. Database migrations
│   │   ├── env.py ........................... Alembic environment configuration
│   │   ├── versions/
│   │   │   └── 001_initial_migration.py .... Initial database schema
│   │   └── alembic.ini ....................... Alembic configuration
│   └── .env ................................ Environment variables
│
└── 📦 Configuration
    ├── requirements.txt ....................... Python dependencies
    └── test_app.py ............................ Validation script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (3.11 recommended)
- MySQL 8.0+
- pip or conda
- Windows, Linux, or macOS

### ⚡ Quick Start (5 minutes)

**Windows PowerShell:**
```powershell
cd "c:\Student Management System"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Linux/macOS:**
```bash
cd ~/path/to/student-management-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Then open your browser to: **http://127.0.0.1:8000**

### Installation (Detailed)

1. **Navigate to project directory**
   ```bash
   cd "c:\Student Management System"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database** (verify .env has correct MySQL credentials)
   ```env
   DATABASE_URL=mysql+mysqlconnector://root:root@localhost:3306/student_management
   SECRET_KEY=thisismystudentmanagementproject
   ```

5. **Start the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Edit `.env` file with your MySQL credentials:
   ```env
   DATABASE_URL=mysql+mysqlconnector://root:your_password@localhost:3306/student_management
   SECRET_KEY=your-super-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Create MySQL database**
   ```bash
   mysql -u root -p
   CREATE DATABASE student_management;
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   python -m app.main
   ```

   The API will be available at: `http://localhost:8000`

### Access API Documentation
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

## 📚 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new admin |
| POST | `/api/auth/login` | Admin login (returns JWT token) |

### Students
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/students` | ✅ | Create student |
| GET | `/api/students` | ✅ | List students (paginated, searchable) |
| GET | `/api/students/{id}` | ✅ | Get student details |
| PUT | `/api/students/{id}` | ✅ | Update student |
| DELETE | `/api/students/{id}` | ✅ | Delete student |
| POST | `/api/students/{id}/courses/{course_id}` | ✅ | Enroll student in course |
| DELETE | `/api/students/{id}/courses/{course_id}` | ✅ | Unenroll student from course |

### Courses
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/courses` | ✅ | Create course |
| GET | `/api/courses` | ✅ | List courses (paginated) |
| GET | `/api/courses/{id}` | ✅ | Get course details |
| PUT | `/api/courses/{id}` | ✅ | Update course |
| DELETE | `/api/courses/{id}` | ✅ | Delete course |

### Attendance
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/attendance` | ✅ | Mark attendance |
| GET | `/api/attendance/{id}` | ✅ | Get attendance record |
| GET | `/api/attendance/student/{student_id}` | ✅ | Get student attendance records |
| GET | `/api/attendance/date/{date}` | ✅ | Get attendance by date |
| GET | `/api/attendance/report/{student_id}/{course_id}` | ✅ | Get attendance report |
| PUT | `/api/attendance/{id}` | ✅ | Update attendance |
| DELETE | `/api/attendance/{id}` | ✅ | Delete attendance |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Login Flow

1. **Register an admin account:**
   ```bash
   POST /api/auth/register
   Content-Type: application/json

   {
     "username": "admin1",
     "email": "admin@example.com",
     "password": "SecurePass123"
   }
   ```

2. **Login to get token:**
   ```bash
   POST /api/auth/login
   Content-Type: application/json

   {
     "username": "admin1",
     "password": "SecurePass123"
   }
   ```

   Response:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer",
     "expires_in": 1800
   }
   ```

3. **Use token in requests:**
   ```bash
   GET /api/students
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

## 💾 Database Schema

### Tables

**admins**
- Admin user accounts with hashed passwords

**students**
- Student information (name, email, phone, address)

**courses**
- Course information (name, code, description, credits)

**student_course** (Junction Table)
- Many-to-many relationship between students and courses

**attendances**
- Attendance records with date, student, course, and status

## 🔄 Database Migrations

### View migration status
```bash
alembic current
```

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## 📝 Example Usage

### 1. Create a Student
```bash
curl -X POST "http://localhost:8000/api/students" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St"
  }'
```

### 2. Create a Course
```bash
curl -X POST "http://localhost:8000/api/courses" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Programming",
    "code": "CS101",
    "description": "Learn Python basics",
    "credits": 3
  }'
```

### 3. Enroll Student in Course
```bash
curl -X POST "http://localhost:8000/api/students/1/courses/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Mark Attendance
```bash
curl -X POST "http://localhost:8000/api/attendance" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "course_id": 1,
    "attendance_date": "2024-01-15T10:00:00Z",
    "is_present": true,
    "remarks": "Present"
  }'
```

### 5. Get Attendance Report
```bash
curl -X GET "http://localhost:8000/api/attendance/report/1/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database Configuration
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/student_management

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Before Production
- Change `SECRET_KEY` to a strong random value: `openssl rand -hex 32`
- Use environment-specific configuration
- Enable HTTPS
- Configure CORS appropriately
- Set up proper logging and monitoring

## 🧪 Testing

The API can be tested using:
- **Swagger UI** at `/api/docs`
- **ReDoc** at `/api/redoc`
- **curl** commands (see examples above)
- **Postman** or similar API clients

## 📋 Best Practices

- All database operations are isolated in the services layer
- All routes protected with JWT except auth endpoints
- Pagination implemented with configurable limits
- Comprehensive error handling with appropriate HTTP status codes
- Logging for all critical operations
- Docstrings on all functions and classes

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL is running
- Check database URL in `.env` file
- Ensure MySQL user has proper permissions

### JWT Token Expired
- Re-login to get a new token
- Token expiry is set to 30 minutes (configurable)

### Migration Errors
- Check Alembic configuration in `alembic/alembic.ini`
- Ensure database URL matches in both `.env` and Alembic config
- Run `alembic stamp head` if migration tables don't exist

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [JWT Introduction](https://jwt.io/introduction)

## 📄 License

This project is provided as-is for educational and commercial use.

## ✅ Project Completion Checklist

- ✅ Database setup with SQLAlchemy ORM
- ✅ Admin authentication with JWT
- ✅ Student management (CRUD)
- ✅ Course management (CRUD)
- ✅ Student-course enrollment (many-to-many)
- ✅ Attendance tracking and reports
- ✅ Comprehensive API documentation
- ✅ Database migrations with Alembic
- ✅ Error handling and logging
- ✅ Pagination support
- ✅ CORS middleware
- ✅ Clean architecture with separation of concerns

---

**Version:** 1.0.0 | **Last Updated:** January 2024