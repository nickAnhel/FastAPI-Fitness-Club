from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///db.sqlite3", echo=False)
session_factory = sessionmaker(bind=engine)
