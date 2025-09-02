from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.Database import db_manager

class DoctorPatientAssignment(db_manager.Base):
  __tablename__ = "doctor_patient_assignments"
  id = Column(Integer, primary_key=True, index=True)
  doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
  patient_uuid = Column(String(36), ForeignKey("patients.patient_uuid"), nullable=False)
  assigned_at = Column(DateTime, default=datetime.utcnow)
  referred_by_doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
  
  doctor = relationship("Doctor", foreign_keys=[doctor_id], back_populates="assignments")
  patient = relationship("Patient", back_populates="assignments")
  referred_by = relationship("Doctor", foreign_keys=[referred_by_doctor_id])
