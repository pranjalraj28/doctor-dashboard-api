from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date_of_visit = Column(DateTime, default=datetime.utcnow)
    observation = Column(Text, nullable=True)
    medicines_prescribed = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="visits")