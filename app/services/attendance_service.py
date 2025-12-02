"""
Attendance service for handling attendance-related business logic.
"""
import logging
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.course import Course
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


logger = logging.getLogger(__name__)


class AttendanceService:
    """Service for attendance operations."""
    
    @staticmethod
    def mark_attendance(db: Session, attendance_data: AttendanceCreate) -> Attendance:
        """
        Mark attendance for a student in a course.
        
        Args:
            db: Database session
            attendance_data: Attendance creation data
            
        Returns:
            Attendance: Created attendance record
        """
        # Verify student exists
        student = db.query(Student).filter(Student.id == attendance_data.student_id).first()
        if not student:
            raise ValueError(f"Student with ID {attendance_data.student_id} not found")
        
        # Verify course exists
        course = db.query(Course).filter(Course.id == attendance_data.course_id).first()
        if not course:
            raise ValueError(f"Course with ID {attendance_data.course_id} not found")
        
        # Check if attendance already marked for this date
        existing = db.query(Attendance).filter(
            and_(
                Attendance.student_id == attendance_data.student_id,
                Attendance.course_id == attendance_data.course_id,
                func.date(Attendance.attendance_date) == attendance_data.attendance_date.date()
            )
        ).first()
        
        if existing:
            raise ValueError("Attendance already marked for this student on this date")
        
        db_attendance = Attendance(
            student_id=attendance_data.student_id,
            course_id=attendance_data.course_id,
            attendance_date=attendance_data.attendance_date,
            is_present=attendance_data.is_present,
            remarks=attendance_data.remarks
        )
        
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        
        logger.info(f"Marked attendance for student {attendance_data.student_id} in course {attendance_data.course_id}")
        return db_attendance
    
    @staticmethod
    def get_attendance_by_id(db: Session, attendance_id: int) -> Attendance | None:
        """
        Get attendance record by ID.
        
        Args:
            db: Database session
            attendance_id: Attendance ID
            
        Returns:
            Attendance: Attendance record or None
        """
        return db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    @staticmethod
    def get_attendance_by_student(db: Session, student_id: int, course_id: int | None = None) -> list[Attendance]:
        """
        Get attendance records for a student.
        
        Args:
            db: Database session
            student_id: Student ID
            course_id: Optional course ID to filter
            
        Returns:
            list: List of attendance records
        """
        query = db.query(Attendance).filter(Attendance.student_id == student_id)
        
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        
        return query.order_by(Attendance.attendance_date.desc()).all()
    
    @staticmethod
    def get_attendance_by_date(db: Session, attendance_date: date, course_id: int | None = None) -> list[Attendance]:
        """
        Get attendance records for a specific date.
        
        Args:
            db: Database session
            attendance_date: Attendance date
            course_id: Optional course ID to filter
            
        Returns:
            list: List of attendance records
        """
        query = db.query(Attendance).filter(
            func.date(Attendance.attendance_date) == attendance_date
        )
        
        if course_id:
            query = query.filter(Attendance.course_id == course_id)
        
        return query.all()
    
    @staticmethod
    def get_attendance_report(db: Session, student_id: int, course_id: int) -> dict:
        """
        Get attendance report for a student in a course.
        
        Args:
            db: Database session
            student_id: Student ID
            course_id: Course ID
            
        Returns:
            dict: Attendance report with statistics
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
        
        attendance_records = db.query(Attendance).filter(
            and_(
                Attendance.student_id == student_id,
                Attendance.course_id == course_id
            )
        ).all()
        
        total_classes = len(attendance_records)
        attended_classes = sum(1 for record in attendance_records if record.is_present)
        
        attendance_percentage = (
            (attended_classes / total_classes * 100) if total_classes > 0 else 0
        )
        
        return {
            "student_id": student_id,
            "student_name": f"{student.first_name} {student.last_name}",
            "course_id": course_id,
            "course_name": course.name,
            "total_classes": total_classes,
            "attended_classes": attended_classes,
            "absent_classes": total_classes - attended_classes,
            "attendance_percentage": round(attendance_percentage, 2)
        }
    
    @staticmethod
    def update_attendance(db: Session, attendance_id: int, attendance_data: AttendanceUpdate) -> Attendance | None:
        """
        Update attendance record.
        
        Args:
            db: Database session
            attendance_id: Attendance ID
            attendance_data: Attendance update data
            
        Returns:
            Attendance: Updated attendance record or None
        """
        attendance = AttendanceService.get_attendance_by_id(db, attendance_id)
        
        if not attendance:
            return None
        
        if attendance_data.is_present is not None:
            attendance.is_present = attendance_data.is_present
        if attendance_data.remarks is not None:
            attendance.remarks = attendance_data.remarks
        
        db.commit()
        db.refresh(attendance)
        
        logger.info(f"Updated attendance record {attendance_id}")
        return attendance
    
    @staticmethod
    def delete_attendance(db: Session, attendance_id: int) -> bool:
        """
        Delete an attendance record.
        
        Args:
            db: Database session
            attendance_id: Attendance ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        attendance = AttendanceService.get_attendance_by_id(db, attendance_id)
        
        if not attendance:
            return False
        
        db.delete(attendance)
        db.commit()
        
        logger.info(f"Deleted attendance record {attendance_id}")
        return True
