from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.Database import db_manager
from app.models.Doctor import Doctor
from app.services.AuthService import auth_service
from app.services.DoctorService import doctor_service
from app.core.exceptions import AuthenticationError

# security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/app/v1/auth/login")
async def get_db_session() -> AsyncGenerator[AsyncSession,None]:
  async for session in db_manager.get_session():
    yield session
    
async def get_current_doctor(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession=Depends(get_db_session)
  ) -> Doctor:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
      payload=auth_service.verify_token(token)
      if payload is None:
        raise credentials_exception
      
      username:str = payload.get("sub")
      doctor_id: int = payload.get("doctor_id")
        
      if username is None or doctor_id is None:
        raise credentials_exception
      doctor = await doctor_service.get_doctor_by_id(db, doctor_id)
      if doctor is None:
        raise credentials_exception
      
      if not doctor.is_active:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Doctor account is inactive"
            )
      return doctor
    except Exception as e:
      if isinstance(e, HTTPException):
            raise e
      raise credentials_exception
  
async def get_active_doctor(
    current_doctor:Doctor=Depends(get_current_doctor)
  ) -> Doctor:
    if not current_doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Doctor account is inactive"
        )
    return current_doctor
           
