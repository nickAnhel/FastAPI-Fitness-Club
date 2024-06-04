from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..config.db_config import session_factory
from ..models.models import ServiceModel, ServiceType
from ..schemas.service_schemas import ServiceCreate
from .base_repository import BaseRepository


class ServiceRepository(BaseRepository):
    def create_all(self) -> None:
        with self._session_factory() as session:
            for service_type in ServiceType:
                service = ServiceModel(service_type=service_type)
                session.add(service)
            session.commit()

    def create(self, data: ServiceCreate) -> ServiceModel:
        with self._session_factory() as session:
            service = ServiceModel(**data.model_dump())
            session.add(service)
            session.commit()
            session.refresh(service)
            return service

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[ServiceModel]:
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

    def get_single(self, **filters) -> ServiceModel:
        with self._session_factory() as session:
            query = select(ServiceModel).filter_by(**filters).options(selectinload(ServiceModel.offices))
            service = session.execute(query).scalar_one()
            return service

    def delete(self, **filters) -> None:
        with self._session_factory() as session:
            service = session.query(ServiceModel).filter_by(**filters).first()
            session.delete(service)
            session.commit()


service_repository = ServiceRepository(session_factory)
