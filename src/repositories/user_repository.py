from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, subqueryload

from ..config.db_config import session_factory
from ..models.models import MembershipModel, UserModel
from ..schemas.user_schemas import UserCreate, UserUpdate
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def create(self, data: UserCreate) -> UserModel:
        with self._session_factory() as session:
            user = UserModel(**data.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_all(
        self,
        *,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[UserModel]:
        with self._session_factory() as session:
            query = (
                select(UserModel)
                .order_by(order)
                .limit(limit)
                .offset(offset)
                .options(subqueryload(UserModel.memberships).subqueryload(MembershipModel.tariff))
            )
            users = session.execute(query).scalars().all()
            return users

    def get_single(self, **fiters) -> UserModel:
        with self._session_factory() as session:
            query = select(UserModel).filter_by(**fiters).options(selectinload(UserModel.memberships))
            user = session.execute(query).scalar_one()
            return user

    def update(self, data: UserUpdate, **filters) -> UserModel:
        with self._session_factory() as session:
            stmt = update(UserModel).values(data.model_dump()).filter_by(**filters).returning(UserModel)
            user = session.execute(stmt).scalar_one()
            session.commit()
            session.refresh(user)
            return user

    def delete(self, **filters) -> None:
        with self._session_factory() as session:
            user = session.query(UserModel).filter_by(**filters).first()
            session.delete(user)
            session.commit()


user_repository = UserRepository(session_factory)
