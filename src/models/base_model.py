import datetime
from sqlalchemy import func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from config.database.db import engine


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),  # type: ignore
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),  # type: ignore
        server_onupdate=func.now(),  # type: ignore
    )

    def __repr__(self) -> str:
        res = []
        for key, value in self.__dict__.items():
            if not key.startswith("_") and not isinstance(value, datetime.datetime):
                res.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(res)})"


async def create_tables():
    Base.metadata.create_all(bind=engine)


async def delete_tables():
    Base.metadata.drop_all(bind=engine)
