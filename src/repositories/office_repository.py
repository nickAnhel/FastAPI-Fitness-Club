from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from ..config.db_config import session_factory
from ..models.models import OfficeModel, ServiceModel, ServiceType
from ..schemas.office_schema import OfficeCreate, OfficeUpdate
from .base_repository import BaseRepository


class OfficeRepository(BaseRepository):
    def create(self, data: OfficeCreate):
        with self._session_factory() as session:
            office = OfficeModel(**data.model_dump())
            session.add(office)
            session.commit()
            session.refresh(office)
            return office

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ):
        with self._session_factory() as session:
            query = (
                select(OfficeModel)
                .order_by(order)
                .limit(limit)
                .offset(offset)
                .options(selectinload(OfficeModel.services))
                .options(selectinload(OfficeModel.memberships))
            )
            offices = session.execute(query).scalars().all()
            return offices

    def get_single(self, **filters):
        with self._session_factory() as session:
            query = (
                select(OfficeModel)
                .filter_by(**filters)
                .options(selectinload(OfficeModel.services))
                .options(selectinload(OfficeModel.memberships))
            )
            office = session.execute(query).scalar_one()
            return office

    def update(self, data: OfficeUpdate, **filters):
        with self._session_factory() as session:
            stmt = update(OfficeModel).values(data.model_dump()).filter_by(**filters).returning(OfficeModel)
            office = session.execute(stmt).scalar_one()
            session.commit()
            session.refresh(office)
            return office

    def add_service(self, service_type: ServiceType, **filters):
        with self._session_factory() as session:
            query = (
                select(ServiceModel).filter_by(service_type=service_type)
                # .options(selectinload(ServiceModel.offices))
            )
            service = session.execute(query).scalar_one()

            office = (
                session.query(OfficeModel)
                .filter_by(**filters)
                .options(selectinload(OfficeModel.services))
                .one()
            )
            office.services.append(service)  # type: ignore
            session.commit()
            session.refresh(office)
            return office

    def delete(self, **filters):
        with self._session_factory() as session:
            office = session.query(OfficeModel).filter_by(**filters).first()
            session.delete(office)
            session.commit()


office_repository = OfficeRepository(session_factory)
