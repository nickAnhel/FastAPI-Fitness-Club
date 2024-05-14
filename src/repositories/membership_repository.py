from typing import Sequence
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from config.db_config import session_factory
from models.models import MembershipModel
from schemas.membership_schema import MembershipCreate
from .base_repository import BaseRepository


class MembershipRepository(BaseRepository):
    def create(self, data: MembershipCreate) -> MembershipModel:
        with self._session_factory() as session:
            membersip = MembershipModel(**data.model_dump())
            session.add(membersip)
            session.commit()
            session.refresh(membersip)
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
            )
            membersip = session.execute(query).unique().scalar_one()
            return membersip

    def delete(self, **filters) -> None:
        with self._session_factory() as session:
            stmt = delete(MembershipModel).filter_by(**filters)
            session.execute(stmt)
            session.commit()


membership_repository = MembershipRepository(session_factory)
