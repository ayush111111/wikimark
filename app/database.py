from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, Column, String, JSON, ForeignKey
from fastapi_users_db_sqlalchemy import GUID
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://auth_user:securepassword@localhost:5432/auth_db")


class Base(DeclarativeBase):
    pass

#  UUID is the primary key ID for user.
class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    tags = Column(JSON, nullable=False) # JSON List

    user_id = Column(GUID, ForeignKey("user.id"))


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
