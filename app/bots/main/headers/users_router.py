from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine
from app.models import User


router = Router()

@router.message(CommandStart())
async def comm_start(message: types.Message):

    async with AsyncSession(engine) as session:
        statement = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(statement)
        db_user = result.scalar_one_or_none()

        if not db_user:
            
            db_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name
            )
            
            session.add(db_user)
            
            await session.commit()
            
            text = f"Приятно познакомиться, {message.from_user.first_name}! Ты внесен в базу клиентов."
        else:
            
            text = f"Рад видеть тебя снова, {message.from_user.first_name}!"

    
    await message.answer(text)