from datetime import datetime, timedelta
import enum

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from backend.config import POSTGRES_URL, IS_PRODUCTION

engine = create_async_engine(POSTGRES_URL, echo=not IS_PRODUCTION)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()


class UserRole(enum.Enum):
    """
    2: Administrator, 1: Moderator, 0: User
    """
    ADMIN = 2
    MODERATOR = 1
    USER = 0

    def __int__(self):
        return self.value


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
    login_limit = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True)
    token = Column(String(4096), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.now() + timedelta(days=1))


class Dataset(Base):
    __tablename__ = 'dataset'

    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    corrected = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete=None))