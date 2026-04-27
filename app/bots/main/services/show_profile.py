from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.users import User, Weightloss, Modes, Improvement
from app.bots.main.keyboards.inlines import get_start_keyboard
from app.bots.main.services.clean_chat import clean_chat
from app.database import engine
from app.bots.main.keyboards.inlines import delete_registr
router = Router()


async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
@router.callback_query(F.data == "my_profile")
async def show_my_profile(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    
    async with async_session() as session:

        user_stmt = select(User).where(User.telegram_id == callback.from_user.id)
        user_res = await session.execute(user_stmt)
        user = user_res.scalar_one_or_none()

        if not user:
            sent_msg = await callback.message.answer("Вы еще не прошли анкету.")
            await state.update_data(last_msg_id=sent_msg.message_id)
            return
        if user:
            profile_text = (
                f"<b>📋 Ваша анкета:</b>\n\n"
                f"👤 <b>ФИО:</b> {user.fio}\n"
                f"🎂 <b>Возраст:</b> {user.age}\n"
                f"📏 <b>Рост:</b> {user.height}\n"
                f"⚖️ <b>Вес:</b> {user.weight}\n"
                f"📧 <b>Email:</b> {user.mail}\n"
            )

            if user.weight_loss:
                loss_stmt = select(Weightloss).where(Weightloss.users_tg == user.telegram_id)
                loss_res = await session.execute(loss_stmt)
                loss_data = loss_res.scalar_one_or_none()
                
                if loss_data:
                    profile_text += (
                        f"\n<b>🎯 Цель: Похудение</b>\n"
                        f"📉 <b>Хочет сбросить:</b> {loss_data.how_kg} кг\n"
                        f"🍽 <b>Приемов пищи:</b> {loss_data.how_eat}\n"
                        f"🏃 <b>Активность:</b> {loss_data.how_active} раз(а) в неделю\n"
                        f"💧 <b>Вода:</b> {loss_data.how_water}\n"
                        f"😴 <b>Сон:</b> {loss_data.how_sleep}"
                    )

            elif user.improve_ment:
                imp_stmt = select(Improvement).where(Improvement.users_tg == user.telegram_id)
                imp_res = await session.execute(imp_stmt)
                imp_data = imp_res.scalar_one_or_none()
                
                if imp_data:
                    profile_text += (
                        f"\n<b>🩺 Цель: Улучшение состояния</b>\n"
                        f"📝 <b>Проблема:</b> {imp_data.problem}"
                    )

            elif user.mode:
                mode_stmt = select(Modes).where(Modes.users_tg == user.telegram_id)
                mode_res = await session.execute(mode_stmt)
                mode_data = mode_res.scalar_one_or_none()
                
                if mode_data:
                    profile_text += (
                        f"\n<b>🎯 Цель: Наладить режим</b>\n"
                        f"📉 <b>Есть ли лишний вес?:</b> {mode_data.have_kg} \n"
                        f"🍽 <b>Приемов пищи:</b> {mode_data.how_eat}\n"
                        f"🏃 <b>Активность:</b> {mode_data.how_active} раз(а) в неделю\n"
                        f"💧 <b>Вода:</b> {mode_data.how_water}\n"
                        f"😴 <b>Сон:</b> {mode_data.how_sleep}"
                    )
        
            await callback.message.edit_text(
            profile_text, 
            parse_mode="HTML", 
            reply_markup=delete_registr() 
        )

@router.callback_query(F.data == "delete_profile")
async def delete_profile_handler(callback: types.CallbackQuery, state: FSMContext):
    if not await clean_chat(callback, state):
        return
    
    await callback.message.delete()
    
    user_id = callback.from_user.id
    
    async with async_session() as session:
        async with session.begin():

            
            await session.execute(delete(Weightloss).where(Weightloss.users_tg == user_id))
            await session.execute(delete(Improvement).where(Improvement.users_tg == user_id))
            await session.execute(delete(Modes).where(Modes.users_tg == user_id))

            await session.execute(delete(User).where(User.telegram_id == user_id))

        await session.commit()

    await state.clear()
    
    await callback.message.answer(
        "<b>Ваша анкета успешно удалены из базы. ✅</b>\n"
        "Вы можете заполнить её снова, нажав: /start.",
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_main_fst")
async def back_to_main_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    sent_msg = await callback.message.edit_text(
        f"Привет👋, меня зовут Ковыршина Валерия! \n\n"
        "Я професcиональный нутрициолог, это мой бот(помощник) который будет присылать вам полезные советы " \
        "и служит для анкетирования и записи моих клиентов, также ты можешь попробовать заполнить анкету, если тебе вдруг интересно работать со мной в будущем \n\n"
        "Я помогу тебе следить за питанием. Для начала нужно заполнить анкету.\n",
        reply_markup=get_start_keyboard()
    )
    await state.update_data(last_msg_id=sent_msg.message_id)



async def send_profile_info(event: types.Message | types.CallbackQuery, user_id: int):
    async with async_session() as session:

        user_stmt = select(User).where(User.telegram_id == user_id)
        user = (await session.execute(user_stmt)).scalar_one_or_none()
        if user:
            profile_text = (
                f"<b>📋 Ваша анкета:</b>\n\n"
                f"👤 <b>ФИО:</b> {user.fio}\n"
                f"🎂 <b>Возраст:</b> {user.age}\n"
                f"📏 <b>Рост:</b> {user.height}\n"
                f"⚖️ <b>Вес:</b> {user.weight}\n"
                f"📧 <b>Email:</b> {user.mail}\n"
            )

            if user.weight_loss:
                loss_stmt = select(Weightloss).where(Weightloss.users_tg == user.telegram_id)
                loss_res = await session.execute(loss_stmt)
                loss_data = loss_res.scalar_one_or_none()
                
                if loss_data:
                    profile_text += (
                        f"\n<b>🎯 Цель: Похудение</b>\n"
                        f"📉 <b>Хочет сбросить:</b> {loss_data.how_kg} кг\n"
                        f"🍽 <b>Приемов пищи:</b> {loss_data.how_eat}\n"
                        f"🏃 <b>Активность:</b> {loss_data.how_active} раз(а) в неделю\n"
                        f"💧 <b>Вода:</b> {loss_data.how_water}\n"
                        f"😴 <b>Сон:</b> {loss_data.how_sleep}"
                    )

            elif user.improve_ment:
                imp_stmt = select(Improvement).where(Improvement.users_tg == user.telegram_id)
                imp_res = await session.execute(imp_stmt)
                imp_data = imp_res.scalar_one_or_none()
                
                if imp_data:
                    profile_text += (
                        f"\n<b>🩺 Цель: Улучшение состояния</b>\n"
                        f"📝 <b>Проблема:</b> {imp_data.problem}"
                    )

            elif user.mode:
                mode_stmt = select(Modes).where(Modes.users_tg == user.telegram_id)
                mode_res = await session.execute(mode_stmt)
                mode_data = mode_res.scalar_one_or_none()
                
                if mode_data:
                    profile_text += (
                        f"\n<b>🎯 Цель: Наладить режим</b>\n"
                        f"📉 <b>Есть ли лишний вес?:</b> {mode_data.have_kg} \n"
                        f"🍽 <b>Приемов пищи:</b> {mode_data.how_eat}\n"
                        f"🏃 <b>Активность:</b> {mode_data.how_active} раз(а) в неделю\n"
                        f"💧 <b>Вода:</b> {mode_data.how_water}\n"
                        f"😴 <b>Сон:</b> {mode_data.how_sleep}"
                    )
        
            if isinstance(event, types.Message):
                await event.answer(profile_text, parse_mode="HTML", reply_markup=delete_registr())
            else:
                await event.message.edit_text(profile_text, parse_mode="HTML", reply_markup=delete_registr())