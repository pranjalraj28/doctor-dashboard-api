from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.Doctor import Doctor
from app.schemas.DoctorSchema import DoctorCreate, DoctorUpdate
from app.services.AuthService import auth_service
from app.core.exceptions import DoctorNotFoundError, DuplicateError

class DoctorService:
  async def create_doctor(
    self,
    db:AsyncSession,
    doctor_data:DoctorCreate
  )-> Doctor:
    try:
      hashed_password=auth_service.hash_passwords(doctor_data.password)
      db_doctor = Doctor(
        username=doctor_data.username,
        email=doctor_data.email,
        hashed_password=hashed_password,
        first_name=doctor_data.first_name,
        last_name=doctor_data.last_name,
        phone_number=doctor_data.phone_number,
        specialization=doctor_data.specialization,   
      )
      db.add(db_doctor)
      await db.commit()
      await db.refresh(db_doctor)
      return db_doctor
    except IntegrityError as e:
      await db.rollback()
      if "username" in str(e.orig):
          raise DuplicateError("Username already exists")
      elif "email" in str(e.orig):
          raise DuplicateError("Email already exists")
      else:
        raise DuplicateError("Doctor with this information already exists")
  
  async def get_doctor_by_username(
        self, 
        db: AsyncSession, 
        username: str
    ) -> Optional[Doctor]:
        """Get a doctor by username."""
        result = await db.execute(
            select(Doctor).where(Doctor.username == username)
        )
        return result.scalar_one_or_none()
    
  async def get_doctor_by_id(
        self, 
        db: AsyncSession, 
        doctor_id: int
    ) -> Optional[Doctor]:
        """Get a doctor by ID."""
        result = await db.execute(
            select(Doctor).where(Doctor.id == doctor_id)
        )
        return result.scalar_one_or_none()
    
  async def get_doctor_by_email(
        self, 
        db: AsyncSession, 
        email: str
    ) -> Optional[Doctor]:
        """Get a doctor by email."""
        result = await db.execute(
            select(Doctor).where(Doctor.email == email)
        )
        return result.scalar_one_or_none()
      
  async def authenticate_doctor(
        self, 
        db: AsyncSession, 
        username: str, 
        password: str
    ) -> Optional[Doctor]:
        """Authenticate a doctor with username and password."""
        doctor = await self.get_doctor_by_username(db, username)
        
        if not doctor:
            return None
        
        if not doctor.is_active:
            return None
        
        if not auth_service.verify_password(password, doctor.hashed_password):
            return None
        
        return doctor
      
  async def update_doctor(
        self, 
        db: AsyncSession, 
        doctor_id: int, 
        doctor_update: DoctorUpdate
    ) -> Optional[Doctor]:
        """Update doctor information."""
        doctor = await self.get_doctor_by_id(db, doctor_id)
        
        if not doctor:
            raise DoctorNotFoundError("Doctor not found")
        
        # Update only provided fields
        update_data = doctor_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(doctor, field, value)
        
        await db.commit()
        await db.refresh(doctor)
        
        return doctor

  async def delete_doctor(self, db: AsyncSession, doctor_id: int) -> None:
      """Delete a doctor."""
      doctor = await self.get_doctor_by_id(db, doctor_id)

      if not doctor:
          raise DoctorNotFoundError("Doctor not found")

      await db.delete(doctor)
      await db.commit()
      
doctor_service = DoctorService()
  
  