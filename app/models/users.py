from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Column

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[int] = Field(primary_key=True, default=None)
    telegram_id: int = Field(unique=True, index=True, sa_type=BigInteger)
    tg_username: Optional[str] = Field(default=None)

    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))




