import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)

