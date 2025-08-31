from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class PatientBase(BaseModel):
  name:str
  contact:Optional[str]
  email: Optional[EmailStr]
  age: Optional[int]
  gender: Optional[str]
  disease: Optional[str]
  
class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    status: Optional[str]

class PatientResponse(PatientBase):
    id: int
    doctor_id: int
    created_at: datetime
    status: str

    class Config:
        orm_mode = True
        
class VisitResponse(BaseModel):
    id: int
    date_of_visit: datetime
    observation: Optional[str]
    medicines_prescribed: Optional[str]
    comments: Optional[str]

    class Config:
        orm_mode = True
  