from sqlalchemy import select
from sqlalchemy.orm import selectinload

from config.database.db import session_factory
from models.models import OfficeModel
from .base_repository import BaseRepository


class OfficeRepository(BaseRepository):
    def create(self, data):
        with self._session_factory() as session:
            office = OfficeModel(**data)
            session.add(office)
            session.commit()
            session.refresh(office)
            return office

    def get_all(
        self,
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

    def update(self, data, **filters):
        pass
        # with self._session_factory() as session:
        #     query = (
        #         select(Service)
        #         .filter_by(service_type=service_type)
        #         .options(selectinload(Service.offices))
        #     )
        #     service = session.execute(query).scalar()

        #     office = session.query(Office).filter_by(id=office_id).scalar()
        #     office.services.append(service)  # type: ignore
        #     session.commit()

    def delete(self, **filters):
        with self._session_factory() as session:
            office = session.query(OfficeModel).filter_by(**filters).first()
            session.delete(office)
            session.commit()


office_repository = OfficeRepository(session_factory)
