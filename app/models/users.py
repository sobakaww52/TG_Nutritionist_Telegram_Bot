from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Column
from uuid import UUID

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[UUID] = Field(primary_key=True, default=None)
    telegram_id: int = Field(unique=True, index=True, sa_type=BigInteger)
    tg_username: Optional[str] = Field(default=None, max_length=32, min_length=5)

    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))




