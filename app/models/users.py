from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import BigInteger
from uuid import UUID, uuid4

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    telegram_id: int = Field(unique=True, index=True, sa_type=BigInteger)
    tg_username: Optional[str] = Field(default=None, max_length=32, min_length=5)


    fio: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None, ge=12, le=90)
    height: Optional[int] = Field(default=None, ge=100, le=250)
    weight: Optional[float] = Field(default=None, ge=30.0, le=250.0)
    mail: Optional[str] = Field(default=None)
    
    weight_loss: Optional[bool] = Field(default=False)
    improve_ment: Optional[bool] = Field(default=False)
    mode: Optional[bool] = Field(default=False)

class Weightloss (SQLModel, table=True):
    
    __tablename__ = "weightloss"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    users_tg: int = Field(foreign_key="users.telegram_id")

    how_kg: Optional[int] = Field(default=None)
    how_eat: Optional[int] = Field(default=None, max_length=10)
    how_active: Optional[int] = Field(default=None)
    how_water: Optional[int] = Field(default=None)
    how_sleep: Optional[str] = Field(default=None)

class Improvement (SQLModel, table=True):

    __tablename__ = "improvement"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    users_tg: int = Field(foreign_key="users.telegram_id")

    problem: str = Field(default=None)

class Modes (SQLModel, table=True):
    __tablename__ = "modes"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    users_tg: int = Field(foreign_key="users.telegram_id")

    have_kg: Optional[int] = Field(default=None)
    how_eat: Optional[int] = Field(default=None, max_length=10)
    how_active: Optional[int] = Field(default=None)
    how_water: Optional[int] = Field(default=None)
    how_sleep: Optional[str] = Field(default=None)









