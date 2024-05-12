from sqlalchemy import select
from sqlalchemy.orm import selectinload

from config.database.db import session_factory
from models.models import ServiceModel, ServiceTypes
from .base_repository import BaseRepository


class ServiceRepository(BaseRepository):
    def create_all(self):
        with self._session_factory() as session:
            for service_type in ServiceTypes:
                service = ServiceModel(service_type=service_type)
                session.add(service)
            session.commit()

    def create(self, data):
        with self._session_factory() as session:
            service = ServiceModel(**data)
            session.add(service)
            session.commit()
            session.refresh(service)
            return service

    def get_all(
        self,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ):
        with self._session_factory() as session:
            query = (
                select(ServiceModel)
                .order_by(order)
                .limit(limit)
                .offset(offset)
                .options(selectinload(ServiceModel.offices))
            )
            services = session.execute(query).scalars().all()
            return services

    def get_single(self, **filters):
        with self._session_factory() as session:
            query = select(ServiceModel).filter_by(**filters).options(selectinload(ServiceModel.offices))
            service = session.execute(query).scalar_one_or_none()
            return service

    def delete(self, **filters):
        with self._session_factory() as session:
            service = session.query(ServiceModel).filter_by(**filters).first()
            session.delete(service)
            session.commit()


service_repository = ServiceRepository(session_factory)
