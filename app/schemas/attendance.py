"""
Pydantic schemas for attendance-related API requests and responses.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class AttendanceBase(BaseModel):
    """Base schema for attendance data."""
    student_id: int
    course_id: int
    is_present: bool = True
    remarks: Optional[str] = Field(None, max_length=255)


class AttendanceCreate(AttendanceBase):
    """Schema for creating a new attendance record."""
    attendance_date: datetime


class AttendanceUpdate(BaseModel):
    """Schema for updating attendance record."""
    is_present: Optional[bool] = None
    remarks: Optional[str] = Field(None, max_length=255)


class AttendanceResponse(BaseModel):
    """Schema for attendance response."""
    id: int
    student_id: int
    course_id: int
    attendance_date: datetime
    is_present: bool
    remarks: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AttendanceDetailResponse(AttendanceResponse):
    """Schema for detailed attendance with student and course info."""
    student: Optional['StudentResponse'] = None
    course: Optional['CourseResponse'] = None
    
    class Config:
        from_attributes = True


class AttendanceReportResponse(BaseModel):
    """Schema for attendance report."""
    student_id: int
    student_name: str
    course_id: int
    course_name: str
    total_classes: int
    attended_classes: int
    attendance_percentage: float


class AttendanceByDateResponse(BaseModel):
    """Schema for attendance by date."""
    date: datetime
    course_id: int
    course_name: str
    total_students: int
    present_students: int
    absent_students: int
    attendance_records: List[AttendanceResponse]


# Forward reference resolution (avoid circular import)
from app.schemas.student import StudentResponse
from app.schemas.course import CourseResponse
AttendanceDetailResponse.model_rebuild()
