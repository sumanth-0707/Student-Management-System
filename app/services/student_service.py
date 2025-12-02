"""
Student service for handling student-related business logic.
"""
import logging
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.student import Student, student_course
from app.models.course import Course
from app.schemas.student import StudentCreate, StudentUpdate


logger = logging.getLogger(__name__)


class StudentService:
    """Service for student operations."""
    
    @staticmethod
    def create_student(db: Session, student_data: StudentCreate) -> Student:
        """
        Create a new student.
        
        Args:
            db: Database session
            student_data: Student creation data
            
        Returns:
            Student: Created student instance
        """
        # Check if email already exists
        existing_student = db.query(Student).filter(Student.email == student_data.email).first()
        if existing_student:
            raise ValueError(f"Email '{student_data.email}' already exists")
        
        db_student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email,
            phone=student_data.phone,
            address=student_data.address
        )
        
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        logger.info(f"Created new student: {db_student.first_name} {db_student.last_name}")
        return db_student
    
    @staticmethod
    def get_student_by_id(db: Session, student_id: int) -> Student | None:
        """
        Get student by ID.
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            Student: Student instance or None
        """
        return db.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def get_students(db: Session, skip: int = 0, limit: int = 10) -> tuple[list[Student], int]:
        """
        Get paginated list of students.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            tuple: (students list, total count)
        """
        total = db.query(Student).count()
        students = db.query(Student).offset(skip).limit(limit).all()
        return students, total
    
    @staticmethod
    def search_students(db: Session, search_term: str, skip: int = 0, limit: int = 10) -> tuple[list[Student], int]:
        """
        Search students by name or email.
        
        Args:
            db: Database session
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            tuple: (students list, total count)
        """
        query = db.query(Student).filter(
            or_(
                Student.first_name.ilike(f"%{search_term}%"),
                Student.last_name.ilike(f"%{search_term}%"),
                Student.email.ilike(f"%{search_term}%")
            )
        )
        total = query.count()
        students = query.offset(skip).limit(limit).all()
        return students, total
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_data: StudentUpdate) -> Student | None:
        """
        Update student information.
        
        Args:
            db: Database session
            student_id: Student ID
            student_data: Student update data
            
        Returns:
            Student: Updated student instance or None
        """
        student = StudentService.get_student_by_id(db, student_id)
        
        if not student:
            return None
        
        # Update fields
        if student_data.first_name:
            student.first_name = student_data.first_name
        if student_data.last_name:
            student.last_name = student_data.last_name
        if student_data.email:
            student.email = student_data.email
        if student_data.phone:
            student.phone = student_data.phone
        if student_data.address:
            student.address = student_data.address
        
        db.commit()
        db.refresh(student)
        
        logger.info(f"Updated student: {student.first_name} {student.last_name}")
        return student
    
    @staticmethod
    def delete_student(db: Session, student_id: int) -> bool:
        """
        Delete a student.
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        student = StudentService.get_student_by_id(db, student_id)
        
        if not student:
            return False
        
        db.delete(student)
        db.commit()
        
        logger.info(f"Deleted student with ID: {student_id}")
        return True
    
    @staticmethod
    def enroll_student_in_course(db: Session, student_id: int, course_id: int) -> bool:
        """
        Enroll a student in a course.
        
        Args:
            db: Database session
            student_id: Student ID
            course_id: Course ID
            
        Returns:
            bool: True if enrolled, False if already enrolled
        """
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
        
        # Check if already enrolled
        if course in student.courses:
            return False
        
        student.courses.append(course)
        db.commit()
        
        logger.info(f"Enrolled student {student_id} in course {course_id}")
        return True
    
    @staticmethod
    def unenroll_student_from_course(db: Session, student_id: int, course_id: int) -> bool:
        """
        Unenroll a student from a course.
        
        Args:
            db: Database session
            student_id: Student ID
            course_id: Course ID
            
        Returns:
            bool: True if unenrolled, False if not enrolled
        """
        student = StudentService.get_student_by_id(db, student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise ValueError(f"Course with ID {course_id} not found")
        
        # Check if enrolled
        if course not in student.courses:
            return False
        
        student.courses.remove(course)
        db.commit()
        
        logger.info(f"Unenrolled student {student_id} from course {course_id}")
        return True
