"""
Student router for student management endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin_or_session
from app.models.admin import Admin
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate, StudentListResponse, StudentDetailResponse
from app.services.student_service import StudentService


router = APIRouter(prefix="/api/students", tags=["Students"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Create a new student.
    
    Args:
        student_data: Student creation data
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        StudentResponse: Created student details
    """
    try:
        student = StudentService.create_student(db, student_data)
        return student
    except ValueError as e:
        logger.error(f"Student creation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=StudentListResponse)
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    List all students with pagination and optional search.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records
        search: Optional search term
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        StudentListResponse: Paginated list of students
    """
    if search:
        students, total = StudentService.search_students(db, search, skip, limit)
    else:
        students, total = StudentService.get_students(db, skip, limit)
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "limit": limit,
        "students": students
    }


@router.get("/{student_id}", response_model=StudentDetailResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Get a specific student by ID.
    
    Args:
        student_id: Student ID
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        StudentDetailResponse: Student details with courses
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Update a student.
    
    Args:
        student_id: Student ID
        student_data: Student update data
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        StudentResponse: Updated student details
    """
    student = StudentService.update_student(db, student_id, student_data)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Delete a student.
    
    Args:
        student_id: Student ID
        db: Database session
        current_admin: Current authenticated admin
    """
    deleted = StudentService.delete_student(db, student_id)
    
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


@router.post("/{student_id}/courses/{course_id}", status_code=status.HTTP_200_OK)
def enroll_student(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Enroll a student in a course.
    
    Args:
        student_id: Student ID
        course_id: Course ID
        db: Database session
        current_admin: Current authenticated admin
    """
    try:
        enrolled = StudentService.enroll_student_in_course(db, student_id, course_id)
        
        if not enrolled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is already enrolled in this course"
            )
        
        return {"message": "Student enrolled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{student_id}/courses/{course_id}", status_code=status.HTTP_200_OK)
def unenroll_student(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Unenroll a student from a course.
    
    Args:
        student_id: Student ID
        course_id: Course ID
        db: Database session
        current_admin: Current authenticated admin
    """
    try:
        unenrolled = StudentService.unenroll_student_from_course(db, student_id, course_id)
        
        if not unenrolled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is not enrolled in this course"
            )
        
        return {"message": "Student unenrolled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

