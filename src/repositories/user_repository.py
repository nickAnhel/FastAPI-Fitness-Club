from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.orm import subqueryload
from argon2 import PasswordHasher

from ..config.db_config import session_maker
from ..models.models import MembershipModel
from ..auth.models import UserModel
from ..auth.schemas import UserUpdate, SuperUserCreate
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def create_superuser(self, data: SuperUserCreate) -> UserModel:
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
            query = (
                select(UserModel)
                .filter_by(**fiters)
                .options(subqueryload(UserModel.memberships).subqueryload(MembershipModel.tariff))
            )
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


user_repository = UserRepository(session_maker)
password_hasher = PasswordHasher()


def create_superuser() -> UserModel:
    return user_repository.create_superuser(
        data=SuperUserCreate(
            email="admin@mail.com",
            hashed_password=password_hasher.hash("admin"),
            phone_number="+380000000000",
            first_name="Admin",
            last_name="Admin",
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
    )
