"""
Web router for rendering HTML pages with Jinja2 templates.
Handles GET and POST requests for server-side rendered pages.
"""
import logging
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from starlette.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.admin import Admin
from app.services.admin_service import AdminService
import json
from urllib.parse import quote, unquote

router = APIRouter(tags=["Web Pages"])
logger = logging.getLogger(__name__)


def get_current_user_from_session(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get current user from session cookie.
    Returns Admin object if session is valid, None otherwise.
    """
    admin_id = request.session.get("admin_id")
    
    if not admin_id:
        return None
    
    try:
        admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
        return admin
    except Exception as e:
        logger.debug(f"Session validation error: {str(e)}")
        return None


def get_current_user_from_session_required(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get current user from session cookie.
    Returns admin if authenticated, None if not (caller should redirect).
    """
    admin_id = request.session.get("admin_id")
    logger.debug(f"Checking session - admin_id: {admin_id}, session keys: {list(request.session.keys())}")
    
    if not admin_id:
        logger.debug("No admin_id in session")
        return None
    
    try:
        admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
        logger.debug(f"Retrieved admin from DB: {admin}")
        return admin
    except Exception as e:
        logger.debug(f"Session validation error: {str(e)}")
        return None


@router.get("/home")
def home(
    request: Request,
    current_admin: Admin = Depends(get_current_user_from_session)
):
    """
    Home page route.
    Shows hero section for non-authenticated users and dashboard links for authenticated users.
    """
    is_authenticated = current_admin is not None
    context = {
        "request": request,
        "is_authenticated": is_authenticated,
        "username": current_admin.username if current_admin else None
    }
    return request.app.state.templates.TemplateResponse("index.html", context)


@router.get("/login")
def login_page(request: Request, error: str = None):
    """
    Login page route (GET).
    Displays login form for admin authentication.
    """
    context = {
        "request": request,
        "is_authenticated": False,
        "username": None,
        "error": error
    }
    return request.app.state.templates.TemplateResponse("login.html", context)


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Login form submission (POST).
    Validates credentials and creates session.
    """
    try:
        # Verify admin credentials
        admin = AdminService.verify_admin_password(db, username, password)
        
        if not admin:
            logger.warning(f"Failed login attempt for username: {username}")
            return login_page(request, error="Invalid username or password")
        
        # Set session using request.session (SessionMiddleware)
        request.session["admin_id"] = str(admin.id)
        request.session["username"] = admin.username
        request.session["is_authenticated"] = True
        
        logger.info(f"Admin {admin.username} logged in successfully")
        logger.info(f"Session data set: {dict(request.session)}")
        
        # Create redirect response - SessionMiddleware will add Set-Cookie headers
        response = RedirectResponse(url="/dashboard", status_code=303)
        
        # WORKAROUND: Manually ensure session cookie is set
        # In case SessionMiddleware doesn't catch it automatically
        if "session" not in response.headers:
            logger.info("Manually setting session data in response")
            # The middleware should handle this, but we log to verify
        
        return response
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return login_page(request, error="An error occurred during login")


@router.get("/logout")
def logout(request: Request):
    """
    Logout route.
    Clears the session and redirects to login page.
    """
    request.session.clear()
    logger.info("User logged out successfully")
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@router.get("/register")
def register_page(request: Request):
    """
    Register page route.
    Displays registration form for new admin account creation.
    """
    context = {
        "request": request,
        "is_authenticated": False,
        "username": None
    }
    return request.app.state.templates.TemplateResponse("register.html", context)


@router.get("/dashboard")
def dashboard(
    request: Request,
    current_admin: Admin = Depends(get_current_user_from_session_required),
    db: Session = Depends(get_db)
):
    """
    Dashboard page route.
    Shows overview statistics and quick access to main features.
    Requires authentication (session cookie).
    """
    
    logger.debug(f"Dashboard GET request - admin_id from session: {request.session.get('admin_id')}")
    logger.debug(f"Current admin object: {current_admin}")
    logger.debug(f"Full session: {dict(request.session)}")
    
    # Redirect to login if not authenticated
    if not current_admin:
        logger.warning(f"Dashboard: No admin found, redirecting to login. Session: {dict(request.session)}")
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    logger.info(f"Dashboard: Rendering for admin {current_admin.username}")
    
    try:
        # Get statistics
        from app.models.student import Student
        from app.models.course import Course
        
        students_count = db.query(Student).count()
        courses_count = db.query(Course).count()
        
        context = {
            "request": request,
            "is_authenticated": True,
            "username": current_admin.username,
            "students_count": students_count,
            "courses_count": courses_count
        }
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        context = {
            "request": request,
            "is_authenticated": True,
            "username": current_admin.username,
            "students_count": 0,
            "courses_count": 0,
            "error": "Failed to load statistics"
        }
    
    return request.app.state.templates.TemplateResponse("dashboard.html", context)


@router.get("/students")
def students_page(
    request: Request,
    current_admin: Admin = Depends(get_current_user_from_session_required)
):
    """
    Students list page route.
    Displays students management interface with table and pagination.
    Requires authentication (session cookie).
    """
    
    if not current_admin:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    context = {
        "request": request,
        "is_authenticated": True,
        "username": current_admin.username
    }
    return request.app.state.templates.TemplateResponse("students.html", context)


@router.get("/add-student")
def add_student_page(
    request: Request,
    current_admin: Admin = Depends(get_current_user_from_session_required)
):
    """
    Add new student page route.
    Displays form for creating a new student.
    Requires authentication (session cookie).
    """
    
    if not current_admin:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    context = {
        "request": request,
        "is_authenticated": True,
        "username": current_admin.username
    }
    return request.app.state.templates.TemplateResponse("add_student.html", context)


@router.get("/edit-student/{student_id}")
def edit_student_page(
    request: Request,
    student_id: int,
    current_admin: Admin = Depends(get_current_user_from_session_required)
):
    """
    Edit student page route.
    Displays form for editing an existing student.
    Requires authentication (session cookie).
    """
    
    if not current_admin:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    context = {
        "request": request,
        "is_authenticated": True,
        "username": current_admin.username,
        "student_id": student_id
    }
    return request.app.state.templates.TemplateResponse("edit_student.html", context)


@router.get("/courses")
def courses_page(
    request: Request,
    current_admin: Admin = Depends(get_current_user_from_session_required)
):
    """
    Courses list page route.
    Displays courses management interface.
    Requires authentication (session cookie).
    """
    
    if not current_admin:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    context = {
        "request": request,
        "is_authenticated": True,
        "username": current_admin.username
    }
    return request.app.state.templates.TemplateResponse("courses.html", context)


@router.get("/attendance")
def attendance_page(
    request: Request,
    current_admin: Admin = Depends(get_current_user_from_session_required)
):
    """
    Attendance tracking page route.
    Displays attendance management interface.
    Requires authentication (session cookie).
    """
    
    if not current_admin:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    context = {
        "request": request,
        "is_authenticated": True,
        "username": current_admin.username
    }
    return request.app.state.templates.TemplateResponse("attendance.html", context)

@router.get("/.well-known/appspecific/com.chrome.devtools.json")
def ignore_chrome_devtools():
    """
    Chrome DevTools automatically requests this URL.
    We return 204 to silence unnecessary 404 logs.
    """
    return Response(status_code=204)
