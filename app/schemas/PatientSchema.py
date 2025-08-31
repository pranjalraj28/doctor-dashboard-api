from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GenderEnumPy(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class PatientBase(BaseModel):
  name:str
  contact:Optional[str]
  email: Optional[EmailStr]
  age: Optional[int]
  gender: Optional[GenderEnumPy] = None  
  disease: Optional[str]
  
  @validator("gender", pre=True)
  def normalize_gender(cls, v):
    if isinstance(v, str):
        return v.lower()
    return v
  
class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    contact: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    age: Optional[int] = Field(default=None)
    gender: Optional[GenderEnumPy] = Field(default=None)
    disease: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)

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
  