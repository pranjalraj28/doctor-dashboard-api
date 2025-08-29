from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session, get_current_doctor
from app.models.doctor import Doctor
from app.schemas.doctor_schema import (
    DoctorCreate, 
    DoctorResponse, 
    DoctorLogin, 
    Token, 
    DoctorUpdate
)
from app.services.doctor import doctor_service
from app.services.auth import auth_service
from app.core.exceptions import DuplicateError, DoctorNotFoundError

router = APIRouter(prefix="/auth",tags=["authentication"])

@router.post("register", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_profile(
  doctor_data:DoctorCreate,
  db:AsyncSession=Depends(get_db_session)
):
  try:
    doctor = await doctor_service.create_doctor(db,doctor_data)
    return doctor
  except DuplicateError as e:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
    )
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An error occurred while creating the doctor profile"
    )
    
@router.post("/login", response_model=Token)
async def login_doctor(
    login_data: DoctorLogin,
    db: AsyncSession = Depends(get_db_session)
):
    # Authenticate doctor
  doctor = await doctor_service.authenticate_doctor(
        db, 
        login_data.username, 
        login_data.password
    )
    
  if not doctor:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
  access_token = auth_service.create_token_for_doctor(
        doctor.id, 
        doctor.username
    )
    
  return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=DoctorResponse)
async def get_current_doctor_profile(
    current_doctor: Doctor = Depends(get_current_doctor)
):
    """
    Get the current authenticated doctor's profile.
    
    This endpoint returns the profile information of the currently
    authenticated doctor based on the JWT token.
    """
    return current_doctor
  
@router.put("/me", response_model=DoctorResponse)
async def update_doctor_profile(
    doctor_update: DoctorUpdate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update the current authenticated doctor's profile.
    
    This endpoint allows doctors to update their profile information.
    Only the provided fields will be updated.
    """
    try:
        updated_doctor = await doctor_service.update_doctor(
            db, 
            current_doctor.id, 
            doctor_update
        )
        return updated_doctor
    except DoctorNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the doctor profile"
        )
    
    

