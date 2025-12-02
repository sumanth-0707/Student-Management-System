"""
Main FastAPI application entry point.
Initializes the app, includes all routers, sets up middleware, and exception handlers.
Supports both API endpoints and web-based frontend with Jinja2 templates.
"""
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.database import Base, engine
from app.core.config import settings
from app.routers import auth_router, student_router, course_router, attendance_router, web_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")


# Initialize FastAPI app
app = FastAPI(
    title="Student Management System",
    description="A comprehensive full-stack platform for managing students, courses, and attendance",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# Configure Jinja2 templates
template_dir = Path(__file__).parent / "templates"
app.state.templates = Jinja2Templates(directory=str(template_dir))

# Mount static files (CSS, JS, images)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ---------------------------
# ✅ Correct Middleware Order
# ---------------------------

# 1️⃣ CORS Middleware FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # For production, change to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="session"        # IMPORTANT - only one cookie
)


# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Student Management System is running"
    }


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Student Management System API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "auth": "/api/auth",
            "students": "/api/students",
            "courses": "/api/courses",
            "attendance": "/api/attendance"
        }
    }


# Include routers
app.include_router(web_router.router)      # Web routes (HTML templates)
app.include_router(auth_router.router)     # Auth API
app.include_router(student_router.router)  # Students API
app.include_router(course_router.router)   # Courses API
app.include_router(attendance_router.router)  # Attendance API


logger.info("FastAPI application initialized successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
