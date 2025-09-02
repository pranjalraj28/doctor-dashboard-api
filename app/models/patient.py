from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.Database import db_manager
import enum
import uuid

class GenderEnum(str,enum.Enum):
  MALE = "male"
  FEMALE = "female"
  OTHER = "other"
  
class Patient(db_manager.Base):
  __tablename__ = "patients"
  id = Column(Integer, primary_key=True, index=True)
  patient_uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()), nullable=False)
  name = Column(String(100), nullable=False)  
  contact = Column(String(100),nullable=True)
  email = Column(String(100), nullable=True)
  age = Column(Integer, nullable=True)
  gender = Column(Enum(GenderEnum, native_enum=False), default=GenderEnum.OTHER)
  disease = Column(String(200), nullable=True)
  # doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  status = Column(String(30), default="active")
  
  
  
  assignments = relationship("DoctorPatientAssignment", back_populates="patient", cascade="all, delete-orphan")
  # doctor = relationship("Doctor", back_populates="patients")
  visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
  