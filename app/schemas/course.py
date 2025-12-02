"""
Pydantic schemas for course-related API requests and responses.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class CourseBase(BaseModel):
    """Base schema for course data."""
    name: str = Field(..., min_length=1, max_length=150)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    credits: int = Field(default=3, ge=1, le=10)


class CourseCreate(CourseBase):
    """Schema for creating a new course."""
    pass


class CourseUpdate(BaseModel):
    """Schema for updating course information."""
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    credits: Optional[int] = Field(None, ge=1, le=10)


class CourseResponse(BaseModel):
    """Schema for course response."""
    id: int
    name: str
    code: str
    description: Optional[str]
    credits: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class CourseDetailResponse(CourseResponse):
    """Schema for detailed course response with enrolled students."""
    students: Optional[List['StudentResponse']] = []
    
    class Config:
        from_attributes = True


# Forward reference resolution (avoid circular import)
from app.schemas.student import StudentResponse
CourseDetailResponse.model_rebuild()
