from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime

from backend.config import POSTGRES_URL, IS_PRODUCTION

engine = create_async_engine(POSTGRES_URL, echo=not IS_PRODUCTION)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False,)
    email = Column(String(255), nullable=False)
    vendor = Column(String(20), nullable=False)
    token = Column(String(255), nullable=False)
    profile = Column(String(4096), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    last_login = Column(DateTime, nullable=False, default=datetime.now())


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.now() + timedelta(days=1))