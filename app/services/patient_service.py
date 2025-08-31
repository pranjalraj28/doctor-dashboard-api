from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate, PatientUpdate
from app.models.doctor import Doctor
class PatientService:
  async def create_patient(
    self,
    db : AsyncSession,
    patient_data : PatientCreate,
    doctor :  Doctor 
  ) -> Patient:
    patient = Patient(**patient_data.model_dump(),doctor_id =doctor.id)
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient

  async def update_patient(self,db: AsyncSession, patient_id: int, patient_update: PatientUpdate, doctor: Doctor) -> Patient | None:
      q = await db.execute(
          select(Patient).where(Patient.id == patient_id, Patient.doctor_id == doctor.id)
      )
      patient = q.scalars().first()
      if not patient:
          return None
      for field, value in patient_update.model_dump(exclude_unset=True).items():
          setattr(patient, field, value)
      await db.commit()
      await db.refresh(patient)
      return patient
    
  async def soft_delete_patient(self,db: AsyncSession, patient_id: int, doctor: Doctor) -> bool:
      q = await db.execute(
          select(Patient).where(Patient.id == patient_id, Patient.doctor_id == doctor.id)
      )
      patient = q.scalars().first()
      if not patient:
          return False
      patient.status = "inactive"
      await db.commit()
      return True
  
patient_service = PatientService()