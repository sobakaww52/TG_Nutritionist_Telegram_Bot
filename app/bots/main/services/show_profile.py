from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from sqlmodel import select, delete


from app.models.users import User, Weightloss, Modes, Improvement
from app.bots.main.keyboards.inlines import get_start_keyboard
from app.bots.main.services.clean_chat import clean_chat
from app.database import async_session, engine
from app.bots.main.keyboards.inlines import delete_registr

router = Router()


@router.callback_query(F.data == "my_profile")
async def show_my_profile(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    
    async with async_session() as session:

        user_stmt = select(User).where(User.telegram_id == callback.from_user.id)
        user_res = await session.execute(user_stmt)
        user = user_res.scalar_one_or_none()

        if not user:
            sent_msg = await callback.message.answer("Вы еще не прошли анкету. /start")
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
    async with async_session() as session:
        result = await session.exec(select(User).where(User.telegram_id == callback.from_user.id))
        user = result.first()

    if not user:
        text = f"""Здравствуйте! Благодарю за проявленный интерес к моему боту — это первый шаг к осознанному отношению к своему здоровью. 

Закрепите бота в своём чате, чтобы регулярно получать:

• актуальную информацию о профильных мероприятиях (вебинары, мастер‑классы, эфиры);

• научно обоснованные статьи по нутрициологии: разбор макро‑ и микронутриентов, их роли в поддержании энергии, качества сна и молодости организма;

• практические гайды: как составить сбалансированный рацион, оптимизировать режим дня и повысить качество жизни;

• эксклюзивные приглашения на образовательные события.

Составляй быстрее анкету, начни наполнятся энергией и двигаться к долгосрочным результатам — с заботой и наукой на вашей стороне 👇 """     
    
    else:
        text = f"""Здравствуйте {user.fio}!👋

Не забудьте закрепить бота в чате, чтобы получать:

• анонсы вебинаров, мастер‑классов и эфиров;

• полезные статьи о нутрициологии и питании;

• гайды по сбалансированному рациону и режиму дня;

• приглашения на эксклюзивные события.

Будем ставить фокус — на питании, восстановлении, энергии и долгосрочных результатах для вашего здоровья."""
    if not await clean_chat(callback, state):
        return   
    sent_msg = await callback.message.edit_text(text, reply_markup=get_start_keyboard())                
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