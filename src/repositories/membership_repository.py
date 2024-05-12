from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from config.database.db import session_factory
from models.models import MembershipModel
from .base_repository import BaseRepository


class MembershipRepository(BaseRepository):
    def create(self, data):
        with self._session_factory() as session:
            membersip = MembershipModel(**data)
            session.add(membersip)
            session.commit()
            session.refresh(membersip)
            return membersip

    def get_all(
        self,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ):
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

    def get_single(self, **filters):
        with self._session_factory() as session:
            query = (
                select(MembershipModel)
                .filter_by(**filters)
                .options(joinedload(MembershipModel.user))
                .options(joinedload(MembershipModel.office))
            )
            membersip = session.execute(query).unique().scalar_one()
            return membersip

    def delete(self, **filters):
        with self._session_factory() as session:
            stmt = delete(MembershipModel).filter_by(**filters)
            session.execute(stmt)
            session.commit()


membership_repository = MembershipRepository(session_factory)
