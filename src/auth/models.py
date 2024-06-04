from typing import Generator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from ..models.base_model import Base
from ..config.db_config import async_session_maker


class UserModel(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str | None]
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    memberships: Mapped[list["MembershipModel"]] = relationship(  # type: ignore
        back_populates="user",
        cascade="all, delete",
    )


async def get_async_session() -> Generator[Session, None, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: Session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserModel)  # type: ignore
