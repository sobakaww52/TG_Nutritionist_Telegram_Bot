from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import BigInteger
from uuid import UUID, uuid4

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    telegram_id: int = Field(unique=True, index=True, sa_type=BigInteger)
    tg_username: Optional[str] = Field(default=None, max_length=32, min_length=5)

    first_name: Optional[str] = Field(default=None, max_length=32)
    age: Optional[int] = Field(default=None, ge=12, le=90)
    weight: Optional[float] = Field(default=None, ge=30.0, le=250.0)
    height: Optional[int] = Field(default=None, ge=100, le=250)
    
    






