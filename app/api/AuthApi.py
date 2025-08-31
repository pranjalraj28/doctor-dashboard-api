from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session
from app.schemas.DoctorSchema import (
    DoctorCreate, 
    DoctorResponse, 
    DoctorLogin, 
    Token
)
from app.services.DoctorService import doctor_service
from app.services.AuthService import auth_service
from app.core.exceptions import DuplicateError
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth",tags=["authentication"])

@router.post("/register", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
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
    form_data: OAuth2PasswordRequestForm = Depends(),    
    db: AsyncSession = Depends(get_db_session)
):
    # Authenticate doctor
  doctor = await doctor_service.authenticate_doctor(
        db, 
        form_data.username, 
        form_data.password
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
    
    

