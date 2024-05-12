from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from config.database.db import session_factory
from models.models import UserModel
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def create(self, data):
        with self._session_factory() as session:
            user = UserModel(**data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_all(
        self,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
    ):
        with self._session_factory() as session:
            query = (
                select(UserModel)
                .order_by(order)
                .limit(limit)
                .offset(offset)
                .options(selectinload(UserModel.memberships))
            )
            users = session.execute(query).scalars().all()
            return users

    def get_single(self, **fiters):
        with self._session_factory() as session:
            query = select(UserModel).filter_by(**fiters).options(selectinload(UserModel.memberships))
            user = session.execute(query).scalar_one()
            return user

    def update(self, data, **filters):
        with self._session_factory() as session:
            stmt = update(UserModel).values(**data).filter_by(**filters).returning(UserModel)
            user = session.execute(stmt).scalar_one()
            session.flush()
            session.commit()
            return user

    def delete(self, **filters):
        with self._session_factory() as session:
            user = session.query(UserModel).filter_by(**filters).first()
            session.delete(user)
            session.commit()


user_repository = UserRepository(session_factory)
