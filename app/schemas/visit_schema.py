from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitBase(BaseModel):
    observation: Optional[str]
    medicines_prescribed: Optional[str]
    comments: Optional[str]

class VisitCreate(VisitBase):
    pass

class VisitUpdate(VisitBase):
    pass

class VisitResponse(VisitBase):
    id: int
    date_of_visit: datetime

    class Config:
        orm_mode = True