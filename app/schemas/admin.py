"""
Pydantic schemas for admin-related API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class AdminBase(BaseModel):
    """Base schema for admin data."""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


class AdminCreate(AdminBase):
    """Schema for creating a new admin."""
    password: str = Field(..., min_length=8)


class AdminUpdate(BaseModel):
    """Schema for updating admin information."""
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class AdminResponse(AdminBase):
    """Schema for admin response."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    """Schema for admin login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for token data."""
    admin_id: Optional[int] = None
