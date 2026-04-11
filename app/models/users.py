from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import BigInteger
from uuid import UUID, uuid4

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    telegram_id: int = Field(unique=True, index=True, sa_type=BigInteger)
    tg_username: Optional[str] = Field(default=None, max_length=32, min_length=5)





