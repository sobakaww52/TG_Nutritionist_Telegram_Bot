import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config import settings
from app.models import User

engine = create_async_engine(settings.database_url, echo=True, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())