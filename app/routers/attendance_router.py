"""
Attendance router for attendance management endpoints.
"""
import logging
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin_or_session
from app.models.admin import Admin
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate, AttendanceDetailResponse
from app.services.attendance_service import AttendanceService


router = APIRouter(prefix="/api/attendance", tags=["Attendance"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Mark attendance for a student in a course.
    
    Args:
        attendance_data: Attendance data
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        AttendanceResponse: Created attendance record
    """
    try:
        attendance = AttendanceService.mark_attendance(db, attendance_data)
        return attendance
    except ValueError as e:
        logger.error(f"Attendance marking error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{attendance_id}", response_model=AttendanceDetailResponse)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Get an attendance record by ID.
    
    Args:
        attendance_id: Attendance ID
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        AttendanceDetailResponse: Attendance record details
    """
    attendance = AttendanceService.get_attendance_by_id(db, attendance_id)
    
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    
    return attendance


@router.get("/student/{student_id}", response_model=list[AttendanceResponse])
def get_student_attendance(
    student_id: int,
    course_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Get attendance records for a student.
    
    Args:
        student_id: Student ID
        course_id: Optional course ID to filter
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        list: List of attendance records
    """
    attendance_records = AttendanceService.get_attendance_by_student(db, student_id, course_id)
    return attendance_records


@router.get("/date/{attendance_date}", response_model=list[AttendanceResponse])
def get_attendance_by_date(
    attendance_date: date,
    course_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Get attendance records for a specific date.
    
    Args:
        attendance_date: Attendance date
        course_id: Optional course ID to filter
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        list: List of attendance records
    """
    attendance_records = AttendanceService.get_attendance_by_date(db, attendance_date, course_id)
    return attendance_records


@router.get("/report/{student_id}/{course_id}")
def get_attendance_report(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Get attendance report for a student in a course.
    
    Args:
        student_id: Student ID
        course_id: Course ID
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        dict: Attendance report with statistics
    """
    try:
        report = AttendanceService.get_attendance_report(db, student_id, course_id)
        return report
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Update an attendance record.
    
    Args:
        attendance_id: Attendance ID
        attendance_data: Attendance update data
        db: Database session
        current_admin: Current authenticated admin
        
    Returns:
        AttendanceResponse: Updated attendance record
    """
    attendance = AttendanceService.update_attendance(db, attendance_id, attendance_data)
    
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    
    return attendance


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_session)
):
    """
    Delete an attendance record.
    
    Args:
        attendance_id: Attendance ID
        db: Database session
        current_admin: Current authenticated admin
    """
    deleted = AttendanceService.delete_attendance(db, attendance_id)
    
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")

