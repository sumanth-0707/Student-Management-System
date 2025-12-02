"""
Attendance model for tracking student attendance.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Attendance(Base):
    """Attendance model tracking student attendance in courses."""
    
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    attendance_date = Column(DateTime(timezone=True), nullable=False, index=True)
    is_present = Column(Boolean, default=True, nullable=False)
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, course_id={self.course_id}, date={self.attendance_date})>"
