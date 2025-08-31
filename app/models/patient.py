from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.Database import Base
import enum

class GenderEnum(str,enum.Enum):
  MALE = "male"
  FEMALE = "female"
  OTHER = "other"
  
class Patient(Base):
  __tablename__ = "patients"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100), nullable=False)  
  contact = Column(String(100),nullable=True)
  email = Column(String(100), nullable=True)
  age = Column(Integer, nullable=True)
  gender = Column(Enum(GenderEnum, native_enum=False), default=GenderEnum.OTHER)
  disease = Column(String(200), nullable=True)
  doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  status = Column(String(30), default="active")
  
  doctor = relationship("Doctor", back_populates="patients")
  visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
  