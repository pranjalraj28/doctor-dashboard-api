import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db_session, get_current_doctor
from app.schemas.PatientSchema import PatientResponse, PatientCreate, PatientUpdate, PatientAssignmentResponse

from app.models.Patient import Patient
from app.models.Doctor import Doctor
from app.services.PatientService import patient_service

router = APIRouter(prefix="/patients", tags=["patients"])

logger = logging.getLogger(__name__)

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
  patient_data : PatientCreate,
  db : AsyncSession = Depends(get_db_session),
  current_doctor = Depends(get_current_doctor)
):
  logger.info(f"Received request to create patient by doctor: {current_doctor.username}")
  patient = await patient_service.create_patient(db,patient_data, current_doctor)
  logger.info(f"Successfully created patient with uuid: {patient.patient_uuid}")
  return patient


@router.get("/{patient_uuid}", response_model=PatientResponse)
async def get_patient(
    patient_uuid: str,
    db: AsyncSession = Depends(get_db_session),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    logger.info(f"Fetching patient with uuid: {patient_uuid} for doctor: {current_doctor.username}")
    patient = await patient_service.get_patient_by_uuid(db, patient_uuid, current_doctor.id)
    if not patient:
        logger.error(f"Patient with uuid: {patient_uuid} not found or unauthorized for doctor: {current_doctor.username}")
        raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
    logger.info(f"Successfully fetched patient with uuid: {patient_uuid}")
    return patient
  
  
@router.post("/{patient_uuid}/assign", response_model=PatientAssignmentResponse)
async def assign_doctor_to_patient(
    patient_uuid: str,
    referred_by: int = None,
    db: AsyncSession = Depends(get_db_session),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    logger.info(f"Assigning doctor: {current_doctor.username} to patient: {patient_uuid}")
    assignment = await patient_service.assign_doctor_to_patient(db, current_doctor.id, patient_uuid, referred_by)
    logger.info(f"Successfully assigned doctor: {current_doctor.username} to patient: {patient_uuid}")
    return assignment
  
@router.get("/{patient_id}",response_model=PatientResponse)
async def get_patient_by_id(
  patient_id:int,
  current_doctor: Doctor = Depends(get_current_doctor),
  db: AsyncSession = Depends(get_db_session)
):
  logger.info(f"Fetching patient with id: {patient_id} for doctor: {current_doctor.username}")
  patient = await patient_service.get_patient_by_id(db,patient_id,current_doctor.id)
  if not patient:
    logger.error(f"Patient with id: {patient_id} not found or unauthorized for doctor: {current_doctor.username}")
    raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
  logger.info(f"Successfully fetched patient with id: {patient_id}")
  return patient
  

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
  patient_id:int,
  patient_update : PatientUpdate,
  db: AsyncSession = Depends(get_db_session),
  current_doctor=Depends(get_current_doctor),
):
  logger.info(f"Updating patient with id: {patient_id} by doctor: {current_doctor.username}")
  patient = await patient_service.update_patient(db, patient_id, patient_update, current_doctor)
  if not patient:
    logger.error(f"Patient with id: {patient_id} not found or unauthorized for doctor: {current_doctor.username}")
    raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
  logger.info(f"Successfully updated patient with id: {patient_id}")
  return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_doctor=Depends(get_current_doctor),
):
    logger.info(f"Soft deleting patient with id: {patient_id} by doctor: {current_doctor.username}")
    success = await patient_service.soft_delete_patient(db, patient_id, current_doctor)
    if not success:
        logger.error(f"Patient with id: {patient_id} not found or unauthorized for soft deletion by doctor: {current_doctor.username}")
        raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
    logger.info(f"Successfully soft deleted patient with id: {patient_id}")
  