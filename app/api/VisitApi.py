import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session, get_current_doctor
from app.schemas.VisitSchema import VisitCreate, VisitUpdate, VisitResponse
from app.services.VisitService import visit_service
from app.models.Doctor import Doctor

router = APIRouter(prefix="/visits", tags=["visits"])

logger = logging.getLogger(__name__)

@router.post(
    "/patient/{patient_uuid}",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_visit(
    patient_uuid: str,
    visit_data: VisitCreate,
    db: AsyncSession = Depends(get_db_session),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    logger.info(f"Received request to create visit for patient: {patient_uuid} by doctor: {current_doctor.username}")
    visit = await visit_service.create_visit(db, patient_uuid, visit_data, current_doctor)
    if not visit:
        logger.error(f"Patient with uuid: {patient_uuid} not found or unauthorized for doctor: {current_doctor.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found or unauthorized",
        )
    logger.info(f"Successfully created visit with id: {visit.id} for patient: {patient_uuid}")
    return visit


@router.get("/{visit_id}", response_model=VisitResponse)
async def get_visit_by_id(
    visit_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db_session),
):
    logger.info(f"Fetching visit with id: {visit_id} for doctor: {current_doctor.username}")
    visit = await visit_service.get_visit_by_id(db, visit_id, current_doctor.id)
    if not visit:
        logger.error(f"Visit with id: {visit_id} not found or unauthorized for doctor: {current_doctor.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found or unauthorized",
        )
    logger.info(f"Successfully fetched visit with id: {visit_id}")
    return visit


@router.put("/{visit_id}", response_model=VisitResponse)
async def update_visit(
    visit_id: int,
    visit_update: VisitUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    logger.info(f"Updating visit with id: {visit_id} by doctor: {current_doctor.username}")
    visit = await visit_service.update_visit(db, visit_id, visit_update, current_doctor)
    if not visit:
        logger.error(f"Visit with id: {visit_id} not found or unauthorized for doctor: {current_doctor.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found or unauthorized",
        )
    logger.info(f"Successfully updated visit with id: {visit_id}")
    return visit


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visit(
    visit_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    logger.info(f"Deleting visit with id: {visit_id} by doctor: {current_doctor.username}")
    success = await visit_service.delete_visit(db, visit_id, current_doctor)
    if not success:
        logger.error(f"Visit with id: {visit_id} not found or unauthorized for deletion by doctor: {current_doctor.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found or unauthorized",
        )
    logger.info(f"Successfully deleted visit with id: {visit_id}")
