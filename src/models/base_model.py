import datetime
from sqlalchemy.orm import DeclarativeBase

from ..config.db_config import engine


class Base(DeclarativeBase):
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
