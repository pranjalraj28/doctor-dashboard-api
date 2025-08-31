from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db_session, get_current_doctor
from app.schemas.PatientSchema import PatientResponse, PatientCreate, PatientUpdate
from app.models.Patient import Patient
from app.models.Doctor import Doctor
from app.services.PatientService import patient_service

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
  patient_data : PatientCreate,
  db : AsyncSession = Depends(get_db_session),
  current_doctor = Depends(get_current_doctor)
):
  patient = await patient_service.create_patient(db,patient_data, current_doctor)
  return patient

@router.get("/{patient_id}",response_model=PatientResponse)
async def get_patient_by_id(
  patient_id:int,
  current_doctor: Doctor = Depends(get_current_doctor),
  db: AsyncSession = Depends(get_db_session)
):
  patient = await patient_service.get_patient_by_id(db,patient_id,current_doctor.id)
  if not patient:
    raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
  return patient
  

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
  patient_id:int,
  patient_update : PatientUpdate,
  db: AsyncSession = Depends(get_db_session),
  current_doctor=Depends(get_current_doctor),
):
  patient = await patient_service.update_patient(db, patient_id, patient_update, current_doctor)
  if not patient:
    raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
  return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_doctor=Depends(get_current_doctor),
):
    success = await patient_service.soft_delete_patient(db, patient_id, current_doctor)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
  