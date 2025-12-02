# Student Management System - Full-Stack Setup Guide

## Project Status: ✅ COMPLETE

This is now a **full-stack FastAPI application** with both web frontend and REST API backend.

---

## Quick Start (Windows)

### Prerequisites
- Python 3.8+ (Python 3.11 recommended)
- MySQL Server running on `localhost:3306`
- pip or conda for package management

### Step 1: Set Up Python Environment

#### Option A: Using venv (Recommended)
```powershell
cd "c:\Student Management System"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Option B: Using conda
```powershell
conda create -n sms python=3.11
conda activate sms
pip install -r requirements.txt
```

### Step 2: Configure Database

1. **Ensure MySQL is running** on localhost:3306
2. **Verify .env file** has correct credentials:
   ```env
   DATABASE_URL=mysql+mysqlconnector://root:root@localhost:3306/student_management
   SECRET_KEY=thisismystudentmanagementproject
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Create database** (MySQL will auto-create `student_management` database on first connection)

### Step 3: Run the Application

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 4: Access the Application

- **Web Frontend**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/api/docs
- **Login Page**: http://127.0.0.1:8000/login

---

## Application Architecture

### Frontend (Jinja2 Templates)
- **Home**: `/` - Landing page
- **Login**: `/login` - Admin authentication
- **Dashboard**: `/dashboard` - Statistics and quick access (requires auth)
- **Students**: `/students` - Student CRUD management (requires auth)
- **Add Student**: `/add-student` - New student form (requires auth)
- **Edit Student**: `/edit-student/{id}` - Edit student (requires auth)
- **Courses**: `/courses` - Course management (requires auth)
- **Attendance**: `/attendance` - Attendance tracking (requires auth)

### Static Files
- **CSS**: `/static/css/style.css` - Responsive styling
- **JavaScript**: `/static/js/main.js` - Frontend utilities and API client

### REST API Endpoints

#### Authentication (`/api/auth`)
- `POST /api/auth/register` - Register new admin
- `POST /api/auth/login` - Get JWT token

#### Students (`/api/students`)
- `GET /api/students` - List students (paginated)
- `POST /api/students` - Create student
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student
- `POST /api/students/{id}/courses/{course_id}` - Enroll in course
- `DELETE /api/students/{id}/courses/{course_id}` - Unenroll from course

#### Courses (`/api/courses`)
- `GET /api/courses` - List courses
- `POST /api/courses` - Create course
- `GET /api/courses/{id}` - Get course details
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

#### Attendance (`/api/attendance`)
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/report/{student_id}/{course_id}` - Get attendance report

---

## First-Time Usage

### 1. Register Admin Account

**Via Web UI:**
1. Open http://127.0.0.1:8000/login
2. Click "Register here"
3. Fill in username, email, and password
4. Submit

**Via API:**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "email": "admin@example.com",
    "password": "SecurePass123"
  }'
```

### 2. Login

**Via Web UI:**
1. Go to http://127.0.0.1:8000/login
2. Enter username and password
3. Submit - you'll be redirected to dashboard

**Via API:**
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "password": "SecurePass123"
  }'
```

Returns:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 3. Create Students

**Via Web UI:**
1. Login and go to Students page
2. Click "Add New Student"
3. Fill in student details
4. Submit

**Via API:**
```bash
curl -X POST "http://127.0.0.1:8000/api/students" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "555-1234"
  }'
```

---

## File Structure

```
Student Management System/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── core/
│   │   ├── config.py           # Settings (Pydantic)
│   │   ├── database.py         # SQLAlchemy setup
│   │   └── security.py         # JWT authentication
│   ├── models/
│   │   ├── admin.py            # Admin ORM model
│   │   ├── student.py          # Student ORM model
│   │   ├── course.py           # Course ORM model
│   │   └── attendance.py       # Attendance ORM model
│   ├── schemas/
│   │   ├── admin.py            # Pydantic request/response schemas
│   │   ├── student.py
│   │   ├── course.py
│   │   └── attendance.py
│   ├── services/
│   │   ├── admin_service.py    # Admin business logic
│   │   ├── student_service.py  # Student CRUD
│   │   ├── course_service.py   # Course CRUD
│   │   └── attendance_service.py # Attendance logic
│   ├── routers/
│   │   ├── web_router.py       # Web page routes (Jinja2)
│   │   ├── auth_router.py      # Authentication API
│   │   ├── student_router.py   # Student API
│   │   ├── course_router.py    # Course API
│   │   └── attendance_router.py # Attendance API
│   ├── utils/
│   │   ├── jwt_utils.py        # JWT token handling
│   │   └── hashing.py          # Password hashing
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── layout.html         # Base template
│   │   ├── index.html          # Home page
│   │   ├── login.html          # Login page
│   │   ├── dashboard.html      # Dashboard
│   │   ├── students.html       # Student list
│   │   ├── add_student.html    # Add student form
│   │   ├── edit_student.html   # Edit student form
│   │   ├── courses.html        # Course management
│   │   └── attendance.html     # Attendance tracking
│   └── static/
│       ├── css/
│       │   └── style.css       # Responsive styling
│       ├── js/
│       │   └── main.js         # Frontend utilities
│       └── images/             # Image assets
├── alembic/                    # Database migrations
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | FastAPI | 0.104.1 |
| Template Engine | Jinja2 | 3.1.2 |
| ORM | SQLAlchemy | 2.0.23 |
| Database | MySQL | 8.0+ |
| Data Validation | Pydantic | 2.5.0 |
| Authentication | python-jose | 3.3.0 |
| Password Hashing | Bcrypt/Passlib | 1.7.4 |
| Web Server | Uvicorn | 0.24.0 |
| Migration Tool | Alembic | 1.12.1 |

---

## Environment Variables (.env)

```env
# Database Connection
DATABASE_URL=mysql+mysqlconnector://root:root@localhost:3306/student_management

# JWT Configuration
SECRET_KEY=your-secret-key-here          # Change in production!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

⚠️ **Production Note:** Always generate a strong SECRET_KEY using:
```bash
openssl rand -hex 32
```

---

## Common Commands

### Run Development Server
```powershell
python -m uvicorn app.main:app --reload
```

### Run Production Server
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Run Tests (if available)
```powershell
pytest
```

### Create Database Migration
```powershell
cd alembic
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Access API Documentation
- Swagger UI: http://127.0.0.1:8000/api/docs
- ReDoc: http://127.0.0.1:8000/api/redoc

---

## Troubleshooting

### Error: "No module named 'app'"
**Solution:** Ensure you're running from the project root directory:
```powershell
cd "c:\Student Management System"
python -m uvicorn app.main:app --reload
```

### Error: "Cannot connect to database"
**Solution:** Verify MySQL is running and credentials in .env are correct:
```powershell
# Check MySQL connection
mysql -u root -p -h localhost -e "SHOW DATABASES;"
```

### Error: "Jinja2 template not found"
**Solution:** Ensure template directory structure is correct:
```powershell
cd app/templates
ls  # Should show 9 HTML files
```

### Port 8000 already in use
**Solution:** Use a different port:
```powershell
python -m uvicorn app.main:app --reload --port 8001
```

---

## Next Steps

1. ✅ Start the server
2. ✅ Register an admin account
3. ✅ Login to the web interface
4. ✅ Create and manage students
5. ✅ Create and manage courses
6. ✅ Enroll students in courses
7. ✅ Track attendance

---

## Support

For API documentation, visit: http://127.0.0.1:8000/api/docs

For issues:
1. Check the console output for error messages
2. Verify all dependencies are installed: `pip list`
3. Check that MySQL is running and accessible
4. Ensure all .env variables are correct

---

**Last Updated:** January 2024  
**Version:** 2.0.0 (Full-Stack)
