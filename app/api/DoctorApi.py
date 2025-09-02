import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session, get_current_doctor
from app.models.Doctor import Doctor
from app.schemas.DoctorSchema import DoctorResponse, DoctorUpdate
from app.services.DoctorService import doctor_service
from app.core.exceptions import DoctorNotFoundError

router = APIRouter(prefix="/doctors", tags=["doctors"])

logger = logging.getLogger(__name__)

@router.get("/me", response_model=DoctorResponse)
async def get_current_doctor_profile(
    current_doctor: Doctor = Depends(get_current_doctor)
):
    """
    Get the current authenticated doctor's profile.
    
    This endpoint returns the profile information of the currently
    authenticated doctor based on the JWT token.
    """
    logger.info(f"Fetching profile for doctor: {current_doctor.username}")
    return current_doctor

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor_by_id(
    doctor_id:int,
    current_doctor:Doctor = Depends(get_current_doctor),
    db:AsyncSession = Depends(get_db_session)
):
    logger.info(f"Fetching doctor by id: {doctor_id}")
    if doctor_id != current_doctor.id:
        logger.warning(f"Unauthorized access attempt for doctor_id: {doctor_id} by doctor: {current_doctor.username}")
        raise HTTPException(status_code=403, detail="Not authorized to access this doctor profile")
    doctor = await doctor_service.get_doctor_by_id(db, doctor_id)
    if not doctor:
        logger.error(f"Doctor with id: {doctor_id} not found")
        raise HTTPException(status_code=404, detail="Doctor not found")
    logger.info(f"Successfully fetched doctor with id: {doctor_id}")
    return doctor

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
        logger.info(f"Updating profile for doctor: {current_doctor.username}")
        updated_doctor = await doctor_service.update_doctor(
            db, 
            current_doctor.id, 
            doctor_update
        )
        logger.info(f"Successfully updated profile for doctor: {current_doctor.username}")
        return updated_doctor
    except DoctorNotFoundError as e:
        logger.error(f"Doctor not found while updating profile for doctor: {current_doctor.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.critical(f"An unexpected error occurred while updating profile for doctor: {current_doctor.username}: {e}")
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
        logger.info(f"Deleting profile for doctor: {current_doctor.username}")
        await doctor_service.delete_doctor(db, current_doctor.id)
        logger.info(f"Successfully deleted profile for doctor: {current_doctor.username}")
    except DoctorNotFoundError as e:
        logger.error(f"Doctor not found while deleting profile for doctor: {current_doctor.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.critical(f"An unexpected error occurred while deleting profile for doctor: {current_doctor.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the doctor profile"
        )
