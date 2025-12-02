"""
Course service for handling course-related business logic.
"""
import logging
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


logger = logging.getLogger(__name__)


class CourseService:
    """Service for course operations."""
    
    @staticmethod
    def create_course(db: Session, course_data: CourseCreate) -> Course:
        """
        Create a new course.
        
        Args:
            db: Database session
            course_data: Course creation data
            
        Returns:
            Course: Created course instance
        """
        # Check if course code already exists
        existing_course = db.query(Course).filter(Course.code == course_data.code).first()
        if existing_course:
            raise ValueError(f"Course code '{course_data.code}' already exists")
        
        # Check if course name already exists
        existing_course = db.query(Course).filter(Course.name == course_data.name).first()
        if existing_course:
            raise ValueError(f"Course name '{course_data.name}' already exists")
        
        db_course = Course(
            name=course_data.name,
            code=course_data.code,
            description=course_data.description,
            credits=course_data.credits
        )
        
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        
        logger.info(f"Created new course: {db_course.name} ({db_course.code})")
        return db_course
    
    @staticmethod
    def get_course_by_id(db: Session, course_id: int) -> Course | None:
        """
        Get course by ID.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            Course: Course instance or None
        """
        return db.query(Course).filter(Course.id == course_id).first()
    
    @staticmethod
    def get_all_courses(db: Session, skip: int = 0, limit: int = 10) -> tuple[list[Course], int]:
        """
        Get paginated list of courses.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            tuple: (courses list, total count)
        """
        total = db.query(Course).count()
        courses = db.query(Course).offset(skip).limit(limit).all()
        return courses, total
    
    @staticmethod
    def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> Course | None:
        """
        Update course information.
        
        Args:
            db: Database session
            course_id: Course ID
            course_data: Course update data
            
        Returns:
            Course: Updated course instance or None
        """
        course = CourseService.get_course_by_id(db, course_id)
        
        if not course:
            return None
        
        # Update fields
        if course_data.name:
            course.name = course_data.name
        if course_data.code:
            course.code = course_data.code
        if course_data.description:
            course.description = course_data.description
        if course_data.credits:
            course.credits = course_data.credits
        
        db.commit()
        db.refresh(course)
        
        logger.info(f"Updated course: {course.name}")
        return course
    
    @staticmethod
    def delete_course(db: Session, course_id: int) -> bool:
        """
        Delete a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        course = CourseService.get_course_by_id(db, course_id)
        
        if not course:
            return False
        
        db.delete(course)
        db.commit()
        
        logger.info(f"Deleted course with ID: {course_id}")
        return True
