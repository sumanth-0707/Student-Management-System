"""
Admin service for handling admin-related business logic.
"""
import logging
from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.utils.hashing import hash_password, verify_password


logger = logging.getLogger(__name__)


class AdminService:
    """Service for admin operations."""
    
    @staticmethod
    def create_admin(db: Session, admin_data: AdminCreate) -> Admin:
        """
        Create a new admin user.
        
        Args:
            db: Database session
            admin_data: Admin creation data
            
        Returns:
            Admin: Created admin instance
        """
        # Check if username already exists
        existing_admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
        if existing_admin:
            raise ValueError(f"Username '{admin_data.username}' already exists")
        
        # Check if email already exists
        existing_admin = db.query(Admin).filter(Admin.email == admin_data.email).first()
        if existing_admin:
            raise ValueError(f"Email '{admin_data.email}' already exists")
        
        # Hash password and create admin
        hashed_password = hash_password(admin_data.password)
        db_admin = Admin(
            username=admin_data.username,
            email=admin_data.email,
            hashed_password=hashed_password
        )
        
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        
        logger.info(f"Created new admin: {db_admin.username}")
        return db_admin
    
    @staticmethod
    def get_admin_by_username(db: Session, username: str) -> Admin | None:
        """
        Get admin by username.
        
        Args:
            db: Database session
            username: Admin username
            
        Returns:
            Admin: Admin instance or None
        """
        return db.query(Admin).filter(Admin.username == username).first()
    
    @staticmethod
    def get_admin_by_id(db: Session, admin_id: int) -> Admin | None:
        """
        Get admin by ID.
        
        Args:
            db: Database session
            admin_id: Admin ID
            
        Returns:
            Admin: Admin instance or None
        """
        return db.query(Admin).filter(Admin.id == admin_id).first()
    
    @staticmethod
    def verify_admin_password(db: Session, username: str, password: str) -> Admin | None:
        """
        Verify admin credentials.
        
        Args:
            db: Database session
            username: Admin username
            password: Plain-text password
            
        Returns:
            Admin: Admin instance if credentials are valid, None otherwise
        """
        admin = AdminService.get_admin_by_username(db, username)
        
        if not admin:
            return None
        
        if not verify_password(password, admin.hashed_password):
            return None
        
        return admin
    
    @staticmethod
    def update_admin(db: Session, admin_id: int, admin_data: AdminUpdate) -> Admin | None:
        """
        Update admin information.
        
        Args:
            db: Database session
            admin_id: Admin ID
            admin_data: Admin update data
            
        Returns:
            Admin: Updated admin instance or None
        """
        admin = AdminService.get_admin_by_id(db, admin_id)
        
        if not admin:
            return None
        
        # Update fields
        if admin_data.username:
            admin.username = admin_data.username
        if admin_data.email:
            admin.email = admin_data.email
        if admin_data.password:
            admin.hashed_password = hash_password(admin_data.password)
        
        db.commit()
        db.refresh(admin)
        
        logger.info(f"Updated admin: {admin.username}")
        return admin
