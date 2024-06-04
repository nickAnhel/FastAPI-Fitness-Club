from typing import Sequence
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload

from ..config.db_config import session_maker
from ..models.models import MembershipModel, TariffModel
from ..schemas.membership_schemas import MembershipCreateWithPeriod
from .base_repository import BaseRepository


class MembershipRepository(BaseRepository):
    def create(self, data: MembershipCreateWithPeriod) -> MembershipModel:
        with self._session_factory() as session:
            query = select(TariffModel).filter_by(period=data.period)
            tariff = session.execute(query).scalars().one()

            membersip = MembershipModel(
                **{key: value for key, value in data.model_dump().items() if key != "period"}, tariff_id=tariff.id
            )
            session.add(membersip)
            session.commit()
            session.refresh(membersip)

            tariff.memberships.append(membersip)

            return membersip

    def get_all(
        self,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[MembershipModel]:
        with self._session_factory() as session:
            query = (
                select(MembershipModel)
                .order_by(order)
                .limit(limit)
                .offset(offset)
                .options(joinedload(MembershipModel.user))
                .options(joinedload(MembershipModel.office))
                .options(selectinload(MembershipModel.tariff))
            )
            membersips = session.execute(query).scalars().all()
            return membersips

    def get_single(self, **filters) -> MembershipModel:
        with self._session_factory() as session:
            query = (
                select(MembershipModel)
                .filter_by(**filters)
                .options(joinedload(MembershipModel.user))
                .options(joinedload(MembershipModel.office))
                .options(selectinload(MembershipModel.tariff))
            )
            membersip = session.execute(query).unique().scalar_one()
            return membersip

    def delete(self, **filters) -> None:
        with self._session_factory() as session:
            stmt = delete(MembershipModel).filter_by(**filters)
            session.execute(stmt)
            session.commit()


membership_repository = MembershipRepository(session_maker)
