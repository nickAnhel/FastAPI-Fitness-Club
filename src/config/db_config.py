from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


engine = create_engine("sqlite:///db.sqlite3", echo=False)
session_maker = sessionmaker(bind=engine)

async_engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3", echo=False)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
