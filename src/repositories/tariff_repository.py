from typing import Sequence
from sqlalchemy import select, update

from ..config.db_config import session_factory
from ..models.models import TariffModel
from ..schemas.tariff_schema import TariffCreate
from .base_repository import BaseRepository


class TariffRepository(BaseRepository):
    def create(self, data: TariffCreate):
        with self._session_factory() as session:
            tariff = TariffModel(**data.model_dump())
            session.add(tariff)
            session.commit()
            session.refresh(tariff)
            return tariff

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[TariffModel]:
        with self._session_factory() as session:
            query = select(TariffModel).order_by(order).limit(limit).offset(offset)
            services = session.execute(query).scalars().all()
            return services

    def get_single(self, **filters) -> TariffModel:
        with self._session_factory() as session:
            query = select(TariffModel).filter_by(**filters)
            service = session.execute(query).scalar_one()
            return service

    def update(self, data, **filters) -> TariffModel:
        with self._session_factory() as session:
            stmt = update(TariffModel).values(data.model_dump()).filter_by(**filters).returning(TariffModel)
            tariff = session.execute(stmt).scalar_one()
            session.commit()
            session.refresh(tariff)
            return tariff

    def delete(self, **filters) -> None:
        with self._session_factory() as session:
            tariff = session.query(TariffModel).filter_by(**filters).first()
            session.delete(tariff)
            session.commit()


tariff_repository = TariffRepository(session_factory)
