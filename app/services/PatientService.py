import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Patient import Patient
from app.schemas.PatientSchema import PatientCreate, PatientUpdate
from app.models.Doctor import Doctor
from app.models.DoctorPatientAssignment import DoctorPatientAssignment

logger = logging.getLogger(__name__)

class PatientService:
  async def create_patient(
    self,
    db : AsyncSession,
    patient_data : PatientCreate,
    doctor :  Doctor 
  ) -> Patient:
    logger.info(f"Creating patient for doctor: {doctor.username}")
    patient = Patient(**patient_data.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    
    assignment = DoctorPatientAssignment(doctor_id=doctor.id, patient_uuid=patient.patient_uuid)
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    logger.info(f"Successfully created patient with uuid: {patient.patient_uuid} and assigned to doctor: {doctor.username}")
    return patient

  async def update_patient(self,db: AsyncSession, patient_id: int, patient_update: PatientUpdate, doctor: Doctor) -> Patient | None:
      logger.info(f"Updating patient with id: {patient_id} by doctor: {doctor.username}")
      q = await db.execute(
          select(Patient).where(Patient.id == patient_id, Patient.doctor_id == doctor.id)
      )
      patient = q.scalars().first()
      if not patient:
          logger.error(f"Patient with id: {patient_id} not found or unauthorized for doctor: {doctor.username}")
          return None
      for field, value in patient_update.model_dump(exclude_unset=True).items():
          if value is not None:
              setattr(patient, field, value)
      await db.commit()
      await db.refresh(patient)
      logger.info(f"Successfully updated patient with id: {patient_id}")
      return patient
    
  async def soft_delete_patient(self,db: AsyncSession, patient_id: int, doctor: Doctor) -> bool:
      logger.info(f"Soft deleting patient with id: {patient_id} by doctor: {doctor.username}")
      q = await db.execute(
          select(Patient).where(Patient.id == patient_id, Patient.doctor_id == doctor.id)
      )
      patient = q.scalars().first()
      if not patient:
          logger.error(f"Patient with id: {patient_id} not found or unauthorized for soft deletion by doctor: {doctor.username}")
          return False
      patient.status = "inactive"
      await db.commit()
      logger.info(f"Successfully soft deleted patient with id: {patient_id}")
      return True
  async def get_patient_by_id(
      self,
      db:AsyncSession,
      patient_id:int,
      doctor_id:int
  ) -> Patient | None:
      logger.info(f"Fetching patient by id: {patient_id} for doctor_id: {doctor_id}")
      q = await db.execute(
          select (Patient).where(Patient.id == patient_id, Patient.doctor_id == doctor_id)
      )
      patient = q.scalars().first()
      if not patient:
          logger.error(f"Patient with id: {patient_id} not found or unauthorized for doctor_id: {doctor_id}")
      else:
          logger.info(f"Successfully fetched patient with id: {patient_id}")
      return patient
  
  async def assign_doctor_to_patient(self, db: AsyncSession, doctor_id: int, patient_uuid: str, referred_by: int = None):
        logger.info(f"Assigning doctor_id: {doctor_id} to patient_uuid: {patient_uuid}")
        # Prevent duplicate assignment if desired (left for your implementation)
        assignment = DoctorPatientAssignment(
            doctor_id=doctor_id, patient_uuid=patient_uuid, referred_by_doctor_id=referred_by
        )
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)
        logger.info(f"Successfully assigned doctor_id: {doctor_id} to patient_uuid: {patient_uuid}")
        return assignment
    
  async def get_patient_by_uuid(self, db: AsyncSession, patient_uuid: str, doctor_id: int) -> Patient | None:
        logger.info(f"Fetching patient by uuid: {patient_uuid} for doctor_id: {doctor_id}")
        q = await db.execute(
            select(Patient).join(DoctorPatientAssignment).where(
                Patient.patient_uuid == patient_uuid,
                DoctorPatientAssignment.doctor_id == doctor_id
            )
        )
        patient = q.scalars().first()
        if not patient:
            logger.error(f"Patient with uuid: {patient_uuid} not found or unauthorized for doctor_id: {doctor_id}")
        else:
            logger.info(f"Successfully fetched patient with uuid: {patient_uuid}")
        return patient
    
patient_service = PatientService()