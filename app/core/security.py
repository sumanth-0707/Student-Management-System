"""
Security and authentication configuration.
Handles JWT token dependencies and admin authentication.
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.utils.jwt_utils import decode_token
from app.models.admin import Admin
from app.core.database import get_db


security = HTTPBearer(auto_error=False)


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """
    Dependency to verify JWT token and get current admin.
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        Admin: Current authenticated admin
        
    Raises:
        HTTPException: If token is invalid or admin not found
    """
    token = credentials.credentials
    
    try:
        payload = decode_token(token)
        admin_id: str = payload.get("sub")
        
        if admin_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    
    return admin


async def get_current_admin_or_session(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """
    Dependency to verify authentication via JWT token OR session cookie.
    Accepts both JWT tokens (for API clients) and session cookies (for web browsers).
    
    Args:
        request: FastAPI Request object (for session access)
        credentials: Optional HTTP Bearer credentials
        db: Database session
        
    Returns:
        Admin: Current authenticated admin
        
    Raises:
        HTTPException: If neither JWT token nor session is valid
    """
    admin = None
    
    # Try JWT token first
    if credentials:
        try:
            token = credentials.credentials
            payload = decode_token(token)
            admin_id: str = payload.get("sub")
            
            if admin_id:
                admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
        except Exception:
            pass
    
    # If no JWT, try session cookie
    if not admin:
        admin_id = request.session.get("admin_id")
        if admin_id:
            try:
                admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
            except Exception:
                pass
    
    # If still no admin, raise error
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    return admin
