# AI Coding Agent Instructions - Student Management System

## Project Overview

This is a **production-ready Student Management System backend** built with **FastAPI**, **MySQL**, and **SQLAlchemy ORM**. The system manages students, courses, enrollment relationships, and attendance tracking with JWT-based admin authentication.

**Key Technologies:**
- FastAPI 0.104+ for REST APIs
- SQLAlchemy 2.0+ for ORM with MySQL
- Pydantic 2.0+ for data validation
- JWT authentication with python-jose
- Bcrypt password hashing via passlib
- Alembic for database migrations

---

## Architecture & Project Structure

### Folder Layout
```
app/
├── core/
│   ├── config.py        # Pydantic Settings for env variables
│   ├── database.py      # SQLAlchemy engine, SessionLocal, Base
│   └── security.py      # JWT dependency: get_current_admin()
├── models/
│   ├── admin.py         # Admin ORM model
│   ├── student.py       # Student model + student_course junction table
│   ├── course.py        # Course ORM model
│   └── attendance.py    # Attendance ORM model
├── schemas/
│   ├── admin.py         # AdminCreate, AdminLogin, Token
│   ├── student.py       # StudentCreate, StudentUpdate, StudentResponse
│   ├── course.py        # CourseCreate, CourseUpdate, CourseResponse
│   └── attendance.py    # AttendanceCreate, AttendanceResponse
├── services/
│   ├── admin_service.py      # CRUD + auth logic (verify_password, create_admin)
│   ├── student_service.py    # Student CRUD + enroll/unenroll courses
│   ├── course_service.py     # Course CRUD
│   └── attendance_service.py # Mark attendance + generate reports
├── routers/
│   ├── auth_router.py        # POST /api/auth/login, /api/auth/register
│   ├── student_router.py     # POST/GET/PUT/DELETE /api/students
│   ├── course_router.py      # POST/GET/PUT/DELETE /api/courses
│   └── attendance_router.py  # POST /api/attendance (mark), GET (reports)
├── utils/
│   ├── jwt_utils.py     # create_access_token(), decode_token()
│   └── hashing.py       # hash_password(), verify_password()
├── main.py              # FastAPI app initialization + middleware
└── alembic/
    ├── env.py           # Alembic environment config
    └── versions/        # Migration scripts
```

### Critical Data Flows

**1. Authentication Flow:**
```
POST /api/auth/login → AdminService.verify_admin_password() 
→ jwt_utils.create_access_token() → Return JWT token
```

**2. Student-Course Enrollment:**
- **Many-to-Many Relationship** via `student_course` junction table (SQLAlchemy `association_table`)
- Student CRUD operations in `StudentService`
- Enroll/unenroll via `enroll_student_in_course()` and `unenroll_student_from_course()`

**3. Attendance Workflow:**
```
POST /api/attendance → AttendanceService.mark_attendance() 
→ Validates student + course exist → Creates record with timestamp
→ GET /api/attendance/report/{student_id}/{course_id} → Calculates attendance_percentage
```

---

## Key Conventions & Patterns

### Database Session Management
- **Dependency Injection:** `get_db()` from `app/core/database.py` yields session to routers
- **Pattern:** Every router endpoint includes `db: Session = Depends(get_db)`
- **Auto-cleanup:** Session closed in `finally` block after route completes

### Service Layer Pattern
- **Separation of Concerns:** All DB operations isolated in `services/` (not in routers)
- **Error Handling:** Services raise `ValueError` with descriptive messages
- **Return Types:** Services return ORM models or tuples `(data, total_count)` for pagination
- **Logging:** All critical operations logged via `logger.info()` and `logger.error()`

### Authentication Pattern
- **Decorator Dependency:** `get_current_admin` injected as `current_admin: Admin = Depends(get_current_admin)` on protected routes
- **Token Claims:** JWT contains `"sub": str(admin.id)` 
- **Protected Routes:** All endpoints except `/api/auth/*` require valid JWT

### Pagination Pattern
- **Query Params:** `skip` (default 0) and `limit` (default 10, max 100)
- **Response Model:** `StudentListResponse` contains `total`, `page`, `limit`, `students[]`
- **Service Implementation:** Returns tuple `(results, total_count)` for consistency

### Error Handling Convention
- **HTTPException Status Codes:**
  - `400 BAD_REQUEST` for validation/duplicate errors (ValueError catch)
  - `401 UNAUTHORIZED` for auth failures
  - `404 NOT_FOUND` for missing resources
- **Pattern:** `raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))`

---

## Common Development Workflows

### Adding a New Entity (e.g., "Subject")

1. **Create ORM Model** in `app/models/subject.py`
   ```python
   class Subject(Base):
       __tablename__ = "subjects"
       id = Column(Integer, primary_key=True)
       name = Column(String, unique=True)
       # Add relationships
   ```

2. **Create Pydantic Schemas** in `app/schemas/subject.py`
   ```python
   class SubjectCreate(BaseModel):
       name: str
   class SubjectResponse(BaseModel):
       id: int
       name: str
       class Config:
           from_attributes = True
   ```

3. **Create Service** in `app/services/subject_service.py` with CRUD methods

4. **Create Router** in `app/routers/subject_router.py` following the pattern:
   - Include `get_current_admin` dependency on POST/PUT/DELETE
   - Use service methods for data access
   - Catch ValueError and convert to HTTPException(400)

5. **Register Router** in `app/main.py`:
   ```python
   app.include_router(subject_router.router)
   ```

### Running Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add subject table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing Authentication

1. **Register Admin:**
   ```bash
   POST /api/auth/register
   {"username": "admin1", "email": "admin@example.com", "password": "SecurePass123"}
   ```

2. **Login:**
   ```bash
   POST /api/auth/login
   {"username": "admin1", "password": "SecurePass123"}
   ```
   Returns: `{"access_token": "eyJhbGc...", "token_type": "bearer", "expires_in": 1800}`

3. **Use Token:**
   ```bash
   GET /api/students
   Authorization: Bearer eyJhbGc...
   ```

### Debugging Tips
- Enable SQL logging: Change `echo=False` to `echo=True` in `app/core/database.py`
- Check `.env` file values match your MySQL setup
- Verify admin is active: `Admin.is_active == True`
- JWT expiry: Default 30 minutes from `ACCESS_TOKEN_EXPIRE_MINUTES`

---

## Critical File Dependencies

| If Modifying | Also Update |
|---|---|
| A **model** relationship | Corresponding **schema** relationships (e.g., `courses: List[CourseResponse]`) |
| **Service method signature** | All **router endpoints** calling that method |
| `database.py` config | `.env` file values must match `DATABASE_URL` |
| JWT claims in `create_access_token()` | `decode_token()` and `get_current_admin()` in security.py |
| New **router** | `app/main.py` must include the router via `app.include_router()` |

---

## Performance & Scalability Considerations

- **N+1 Query Prevention:** Use SQLAlchemy `.join()` and `.eager()` for relationships
- **Indexing:** Email, username fields have `index=True` in models
- **Pagination:** Always apply `limit` on list endpoints (max 100)
- **Connection Pooling:** SQLAlchemy uses pool by default; configure in `DATABASE_URL` if needed
- **Logging:** Uses INFO level; set to DEBUG for detailed request/response tracking

---

## Environment Variables (.env)

```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/student_management
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Before Production:** Change `SECRET_KEY` to a strong random value generated by `openssl rand -hex 32`

---

## API Endpoints Quick Reference

| Method | Endpoint | Auth Required | Purpose |
|--------|----------|---|---------|
| POST | `/api/auth/register` | No | Register new admin |
| POST | `/api/auth/login` | No | Get JWT token |
| POST | `/api/students` | Yes | Create student |
| GET | `/api/students?skip=0&limit=10` | Yes | List students (paginated) |
| GET | `/api/students/{id}` | Yes | Get student details |
| POST | `/api/students/{id}/courses/{course_id}` | Yes | Enroll student |
| POST | `/api/courses` | Yes | Create course |
| GET | `/api/courses` | Yes | List courses |
| POST | `/api/attendance` | Yes | Mark attendance |
| GET | `/api/attendance/report/{student_id}/{course_id}` | Yes | Get attendance report |

---

## Example: Typical Feature Implementation

**Scenario:** Add "course_instructor" field to courses

1. Add column to model: `instructor_name = Column(String(100))`
2. Update schemas: Add `instructor_name: str` to `CourseCreate` and `CourseResponse`
3. Update service: `course.instructor_name = course_data.instructor_name` in `update_course()`
4. Router automatically works (no changes needed - Pydantic handles serialization)
5. Create migration: `alembic revision --autogenerate -m "Add instructor_name to courses"`
6. Run migration: `alembic upgrade head`

---

**Last Updated:** January 2024 | **Version:** 1.0.0
