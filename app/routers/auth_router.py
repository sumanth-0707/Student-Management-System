"""
Authentication router for admin login.
"""
import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.admin import AdminLogin, Token, AdminCreate, AdminResponse
from app.services.admin_service import AdminService
from app.utils.jwt_utils import create_access_token
from app.core.config import settings


router = APIRouter(prefix="/api/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=AdminResponse)
def register_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    """
    Register a new admin user.
    
    Args:
        admin_data: Admin registration data
        db: Database session
        
    Returns:
        AdminResponse: Created admin details
    """
    try:
        admin = AdminService.create_admin(db, admin_data)
        return admin
    except ValueError as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
def login(login_data: AdminLogin, db: Session = Depends(get_db)):
    """
    Admin login endpoint.
    
    Args:
        login_data: Admin login credentials
        db: Database session
        
    Returns:
        Token: JWT access token
    """
    admin = AdminService.verify_admin_password(db, login_data.username, login_data.password)
    
    if not admin:
        logger.warning(f"Failed login attempt for username: {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(admin.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Admin {admin.username} logged in successfully")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60
    }
