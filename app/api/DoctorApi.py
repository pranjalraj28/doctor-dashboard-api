from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session, get_current_doctor
from app.models.Doctor import Doctor
from app.schemas.DoctorSchema import DoctorResponse, DoctorUpdate
from app.services.DoctorService import doctor_service
from app.core.exceptions import DoctorNotFoundError

router = APIRouter(prefix="/doctors", tags=["doctors"])

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

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_profile(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete the current authenticated doctor's profile.
    
    This endpoint allows a doctor to delete their own profile.
    This is a permanent action.
    """
    try:
        await doctor_service.delete_doctor(db, current_doctor.id)
    except DoctorNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the doctor profile"
        )
