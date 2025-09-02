import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Visit import Visit
from app.models.DoctorPatientAssignment import DoctorPatientAssignment
from app.schemas.VisitSchema import VisitCreate, VisitUpdate
from app.models.Doctor import Doctor

logger = logging.getLogger(__name__)

class VisitService:

    async def create_visit(
        self,
        db: AsyncSession,
        patient_uuid: str,
        visit_data: VisitCreate,
        doctor: Doctor,
    ) -> Visit | None:
        logger.info(f"Creating visit for patient: {patient_uuid} by doctor: {doctor.username}")
        # Verify that doctor is assigned to patient via assignment table
        q = await db.execute(
            select(DoctorPatientAssignment).where(
                DoctorPatientAssignment.patient_uuid == patient_uuid,
                DoctorPatientAssignment.doctor_id == doctor.id,
            )
        )
        assignment = q.scalars().first()
        if not assignment:
            logger.error(f"Doctor: {doctor.username} is not assigned to patient: {patient_uuid}")
            return None

        # Create visit for the patient and doctor
        visit = Visit(
            patient_uuid=patient_uuid,
            doctor_id=doctor.id,
            **visit_data.model_dump(),
        )
        db.add(visit)
        await db.commit()
        await db.refresh(visit)
        logger.info(f"Successfully created visit with id: {visit.id} for patient: {patient_uuid}")
        return visit

    async def update_visit(
        self,
        db: AsyncSession,
        visit_id: int,
        visit_update: VisitUpdate,
        doctor: Doctor,
    ) -> Visit | None:
        logger.info(f"Updating visit with id: {visit_id} by doctor: {doctor.username}")
        # Fetch visit ensuring it belongs to this doctor
        q = await db.execute(
            select(Visit).where(
                Visit.id == visit_id,
                Visit.doctor_id == doctor.id,
            )
        )
        visit = q.scalars().first()
        if not visit:
            logger.error(f"Visit with id: {visit_id} not found or unauthorized for doctor: {doctor.username}")
            return None

        # Update fields from input where provided
        for field, value in visit_update.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(visit, field, value)

        await db.commit()
        await db.refresh(visit)
        logger.info(f"Successfully updated visit with id: {visit_id}")
        return visit

    async def get_visit_by_id(
        self,
        db: AsyncSession,
        visit_id: int,
        doctor_id: int,
    ) -> Visit | None:
        logger.info(f"Fetching visit by id: {visit_id} for doctor_id: {doctor_id}")
        # Get visit only if current doctor conducted the visit
        q = await db.execute(
            select(Visit).where(
                Visit.id == visit_id,
                Visit.doctor_id == doctor_id,
            )
        )
        visit = q.scalars().first()
        if not visit:
            logger.error(f"Visit with id: {visit_id} not found or unauthorized for doctor_id: {doctor_id}")
        else:
            logger.info(f"Successfully fetched visit with id: {visit_id}")
        return visit

    async def delete_visit(
        self,
        db: AsyncSession,
        visit_id: int,
        doctor: Doctor,
    ) -> bool:
        logger.info(f"Deleting visit with id: {visit_id} by doctor: {doctor.username}")
        # Fetch visit ensuring belongs to doctor for access control
        q = await db.execute(
            select(Visit).where(
                Visit.id == visit_id,
                Visit.doctor_id == doctor.id,
            )
        )
        visit = q.scalars().first()
        if not visit:
            logger.error(f"Visit with id: {visit_id} not found or unauthorized for deletion by doctor: {doctor.username}")
            return False

        await db.delete(visit)
        await db.commit()
        logger.info(f"Successfully deleted visit with id: {visit_id}")
        return True


# Singleton service instance to use in router
visit_service = VisitService()
