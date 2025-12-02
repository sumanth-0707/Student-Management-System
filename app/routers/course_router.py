"""
Course router for course management endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin_or_session
from app.models.admin import Admin
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate, CourseDetailResponse
from app.services.course_service import CourseService


router = APIRouter(prefix="/api/courses", tags=["Courses"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Create a new course.
    
    Args:
        course_data: Course creation data
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        CourseResponse: Created course details
    """
    try:
        course = CourseService.create_course(db, course_data)
        return course
    except ValueError as e:
        logger.error(f"Course creation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[CourseResponse])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    List all courses with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        list: List of courses
    """
    courses, _ = CourseService.get_all_courses(db, skip, limit)
    return courses


@router.get("/{course_id}", response_model=CourseDetailResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Get a specific course by ID.
    
    Args:
        course_id: Course ID
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        CourseDetailResponse: Course details with enrolled students
    """
    course = CourseService.get_course_by_id(db, course_id)
    
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Update a course.
    
    Args:
        course_id: Course ID
        course_data: Course update data
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        CourseResponse: Updated course details
    """
    course = CourseService.update_course(db, course_id, course_data)
    
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Delete a course.
    
    Args:
        course_id: Course ID
        db: Database session
        current_admin: Current authenticated admin
    """
    deleted = CourseService.delete_course(db, course_id)
    
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

