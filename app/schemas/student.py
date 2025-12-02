"""
Pydantic schemas for student-related API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


class StudentBase(BaseModel):
    """Base schema for student data."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=15)
    address: Optional[str] = None


class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating student information."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=15)
    address: Optional[str] = None


class StudentResponse(StudentBase):
    """Schema for student response."""
    id: int
    enrollment_date: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class StudentDetailResponse(StudentResponse):
    """Schema for detailed student response with courses."""
    courses: Optional[List['CourseResponse']] = []
    
    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    """Schema for paginated student list."""
    total: int
    page: int
    limit: int
    students: List[StudentResponse]


# Forward reference resolution
from app.schemas.course import CourseResponse
StudentDetailResponse.model_rebuild()
