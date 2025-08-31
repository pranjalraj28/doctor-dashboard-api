from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependencies import get_db_session, get_current_doctor
from app.schemas.visit_schema import VisitCreate, VisitUpdate, VisitResponse
from app.services.visit_service import visit_service

router = APIRouter(prefix="/visits", tags=["visits"])

@router.post("/patient/{patient_id}", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(
    patient_id: int,
    visit_data: VisitCreate,
    db: AsyncSession = Depends(get_db_session),
    current_doctor=Depends(get_current_doctor),
):
    visit = await visit_service.create_visit(db, patient_id, visit_data, current_doctor)
    if not visit:
        raise HTTPException(status_code=404, detail="Patient not found or unauthorized")
    return visit

@router.put("/{visit_id}", response_model=VisitResponse)
async def update_visit(
    visit_id: int,
    visit_update: VisitUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_doctor=Depends(get_current_doctor),
):
    visit = await visit_service.update_visit(db, visit_id, visit_update, current_doctor)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found or unauthorized")
    return visit

@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visit(
    visit_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_doctor=Depends(get_current_doctor),
):
    success = await visit_service.delete_visit(db, visit_id, current_doctor)
    if not success:
        raise HTTPException(status_code=404, detail="Visit not found or unauthorized")
