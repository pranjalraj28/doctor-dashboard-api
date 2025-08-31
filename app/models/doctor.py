from sqlalchemy import Column, Integer, String, text, DateTime,  Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.Database import Base



class Doctor(Base):
   __tablename__ = "doctors"
   id = Column(Integer, primary_key=True, index=True, autoincrement=True)
   username = Column(String[25], unique=True, index=True, nullable=False)
   email = Column(String[255], unique=True, index=True, nullable=False)
   hashed_password = Column(String(255), nullable=False)
   first_name = Column(String(100), nullable=False)
   last_name = Column(String(100), nullable=False)
   phone_number = Column(String(20), nullable=True)
   specialization = Column(String(100), nullable=False)
   is_active = Column(Boolean, default=True, nullable=False)
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())

   patients = relationship("Patient", back_populates="doctor")