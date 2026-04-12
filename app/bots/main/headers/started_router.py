from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bots.main.keyboards.inlines import get_start_keyboard



router = Router()

@router.message(CommandStart())
async def comm_start(message: types.Message):
    await message.answer(
        f"Привет👋, меня зовут Ковыршина Валерия! \n\n"
        "Я проффесиональный нутрициолог, это мой бот(помощник) который будет присылать вам полезные советы" \
        "и служит для анкетирования и записи моих клиентов, также ты можешь попробовать заполнить анкету, если тебе вдруг интересно работать со мной в будущем \n\n"
        "Я помогу тебе следить за питанием. Для начала нужно заполнить анкету.\n",
        reply_markup=get_start_keyboard()
    )