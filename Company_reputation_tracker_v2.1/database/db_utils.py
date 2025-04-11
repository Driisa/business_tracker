from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schema import Base
from config import DB_URL

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def init_db():
    Base.metadata.create_all(engine)

def get_db_session():
    return SessionLocal()
