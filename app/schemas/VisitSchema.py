from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VisitBase(BaseModel):
    observation: Optional[str]
    medicines_prescribed: Optional[str]
    comments: Optional[str]

class VisitCreate(VisitBase):
    patient_uuid: str
    doctor_id: int

class VisitUpdate(VisitBase):
    observation: Optional[str] = Field(default=None)
    medicines_prescribed: Optional[str] = Field(default=None)
    comments: Optional[str] = Field(default=None)

class VisitResponse(VisitBase):
    id: int
    patient_uuid: str
    doctor_id: int
    date_of_visit: datetime

    class Config:
        orm_mode = True