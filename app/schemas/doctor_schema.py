from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional

class DoctorBase(BaseModel):
  username:str = Field(..., min_length=3, max_length=25, description="Unique username")
  email: EmailStr = Field(..., description="Doctor's email address")
  first_name: str = Field(..., min_length=1, max_length=100, description="Doctor's first name")
  last_name: str = Field(..., min_length=1, max_length=100, description="Doctor's last name")
  phone_number: Optional[str] = Field(None, max_length=20, description="Contact phone number")
  specialization: str = Field(..., min_length=1, max_length=100, description="Medical specialization")
  
class DoctorCreate(DoctorBase):
  password: str = Field(..., min_length=4, description="Password for the account")
  @validator('password')
  def validate_password(cls, v):
        if len(v) < 4:
            raise ValueError('Password must be at least 4 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
    
  @validator('username')
  def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v.lower()
    
  @validator('phone_number')
  def validate_phone(cls, v):
        if v is not None:
            # Remove all non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, v))
            if len(digits_only) < 10:
                raise ValueError('Phone number must contain at least 10 digits')
        return v
  class Config:
        schema_extra = {
            "example": {
                "username": "drjohnsmith",
                "email": "john.smith@hospital.com",
                "password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Smith",
                "phone_number": "+1-234-567-8900",
                "specialization": "Cardiology"
            }
        }


class DoctorUpdate(BaseModel):

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    specialization: Optional[str] = Field(None, min_length=1, max_length=100)
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if v is not None:
            digits_only = ''.join(filter(str.isdigit, v))
            if len(digits_only) < 10:
                raise ValueError('Phone number must contain at least 10 digits')
        return v
    



class DoctorResponse(DoctorBase):
    """Schema for doctor response (excludes sensitive information)."""
    id: int = Field(..., description="Unique doctor ID")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True  # For SQLAlchemy 2.0 compatibility
        schema_extra = {
            "example": {
                "id": 1,
                "username": "drjohnsmith",
                "email": "john.smith@hospital.com",
                "first_name": "John",
                "last_name": "Smith",
                "phone_number": "+1-234-567-8900",
                "specialization": "Cardiology",
                "is_active": True,
                "created_at": "2025-08-27T18:10:00.000Z",
                "updated_at": "2025-08-27T18:10:00.000Z"
            }
        }


class DoctorLogin(BaseModel):
    """Schema for doctor login."""
    username: str = Field(..., description="Doctor's username")
    password: str = Field(..., description="Doctor's password")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "drjohnsmith",
                "password": "SecurePass123!"
            }
        }


class DoctorPublicProfile(BaseModel):
    """Schema for public doctor profile (minimal information)."""
    id: int
    first_name: str
    last_name: str
    specialization: str    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: Optional[int] = Field(None, description="Token expiration time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class TokenData(BaseModel):
    """Schema for token data."""
    username: Optional[str] = None
    doctor_id: Optional[int] = None
    scopes: list[str] = []


class PasswordChange(BaseModel):
    """Schema for changing password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 4:
            raise ValueError('Password must be at least 4 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class DoctorStats(BaseModel):
    """Schema for doctor statistics."""
    total_patients: int = 0
    total_appointments: int = 0
    completed_appointments: int = 0
    pending_appointments: int = 0
    years_of_experience: Optional[int] = None
    
    class Config:
        schema_extra = {
            "example": {
                "total_patients": 150,
                "total_appointments": 500,
                "completed_appointments": 480,
                "pending_appointments": 20,
                "years_of_experience": 15
            }
        }
  