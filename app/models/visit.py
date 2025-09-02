from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.Database import db_manager

class Visit(db_manager.Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    patient_uuid = Column(String(36), ForeignKey("patients.patient_uuid"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    # patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date_of_visit = Column(DateTime, default=datetime.utcnow)
    observation = Column(Text, nullable=True)
    medicines_prescribed = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="visits")
    doctor = relationship("Doctor", back_populates="visits")
