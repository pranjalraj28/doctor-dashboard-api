from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Visit import Visit
from app.models.Patient import Patient
from app.schemas.VisitSchema import VisitCreate, VisitUpdate
from app.models.Doctor import Doctor

class VisitService:
  
  async def create_visit(self,db: AsyncSession, patient_id: int, visit_data: VisitCreate, doctor: Doctor) -> Visit | None:
      # Verify patient belongs to this doctor
      q = await db.execute(
          select(Patient).where(Patient.id == patient_id, Patient.doctor_id == doctor.id)
      )
      patient = q.scalars().first()
      if not patient:
          return None
      visit = Visit(patient_id=patient_id, **visit_data.model_dump())
      db.add(visit)
      await db.commit()
      await db.refresh(visit)
      return visit

  async def update_visit(self,db: AsyncSession, visit_id: int, visit_update: VisitUpdate, doctor: Doctor) -> Visit | None:
      q = await db.execute(
          select(Visit).join(Patient).where(
              Visit.id == visit_id,
              Patient.doctor_id == doctor.id,
          )
      )
      visit = q.scalars().first()
      if not visit:
          return None
      for field, value in visit_update.model_dump(exclude_unset=True).items():
          if value is not None:
              setattr(visit, field, value)
      await db.commit()
      await db.refresh(visit)
      return visit

  async def delete_visit(self,db: AsyncSession, visit_id: int, doctor: Doctor) -> bool:
      q = await db.execute(
          select(Visit).join(Patient).where(
              Visit.id == visit_id,
              Patient.doctor_id == doctor.id,
          )
      )
      visit = q.scalars().first()
      if not visit:
          return False
      await db.delete(visit)
      await db.commit()
      return True

visit_service = VisitService()