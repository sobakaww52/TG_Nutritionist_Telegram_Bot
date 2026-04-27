from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlmodel import select

from app.bots.main.states import RegistrationUsers, RegistationImprovement, RegistationMode, RegistrationWeightloss
from app.models.users import User, Improvement, Weightloss, Modes
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database import engine

from app.bots.main.services.email_validate import validate_email
from app.bots.main.keyboards.inlines import get_finish_keyboard, how_water_keyboard, yes_or_not_keyboard
from app.bots.main.services.clean_chat import clean_chat
from app.bots.main.services.show_profile import send_profile_info

router = Router()


@router.callback_query(F.data == "start_registration")
async def start_survey_first(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if not await clean_chat(callback, state):
        return
    async with async_session() as session:
        statement = select(User).where(User.telegram_id == callback.from_user.id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            # 
            sent_msg = await callback.message.answer(
                "<b>У вас уже есть заполненная анкета!</b>\n\n"
                "Чтобы заполнить её заново, сначала удалите старую анкету в разделе «Моя анкета». /start",
                parse_mode="HTML", 
            )
            await state.update_data(last_msg_id=sent_msg.message_id)
            return
        
    await clean_chat(callback, state)
    
    sent_msg = await callback.message.answer("Введите ваше ФИО:")
    await state.update_data(last_msg_id=sent_msg.message_id)
    await state.set_state(RegistrationUsers.fio)

@router.message(RegistrationUsers.fio)
async def process_fio(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return
        
        await state.update_data(fio=message.text)
        sent_msg = await message.answer("Принято, теперь напиши мне свой возраст:")
        await state.update_data(last_msg_id=sent_msg.message_id)
        await state.set_state(RegistrationUsers.age)
   
    except ValueError:
        await message.answer(
            "Извини, введите корректное имя. 🧐 Например(Артем)\n")
        
@router.message(RegistrationUsers.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return

        age_val = int(message.text)
        if 14 <= age_val <= 90:
            await state.update_data(age=age_val)

            sent_msg =await message.answer("Принято, теперь напиши мне свой рост(см): ")
            await state.update_data(last_msg_id=sent_msg.message_id)

            await state.set_state(RegistrationUsers.height)
        else:
            await message.answer("Возраст должен быть от 14 до 90 лет!")

    except ValueError:
        await message.answer(
            "Извини, но это не похоже на число. 🧐\n"
            "Пожалуйста, введи только цифры (например: 35)")


@router.message(RegistrationUsers.height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return

        height_val = int(message.text)
        if 100 <= height_val <= 250:
            await state.update_data(height=height_val)

            sent_msg = await message.answer("Отлично, теперь напиши мне свой вес(кг): ")
            await state.update_data(last_msg_id=sent_msg.message_id)

            await state.set_state(RegistrationUsers.weight)
        else:
            await message.answer("Рост должен быть от 100 до 250 см. Введи корректный рост:")
    
    except ValueError:
        await message.answer(
            "Извини, но это не похоже на число. 🧐\n"
            "Пожалуйста, введи только цифры (например: 170)")
        
@router.message(RegistrationUsers.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return

        weight_val = float(message.text.replace(",", "."))
        if 40<= weight_val <= 300:
            await state.update_data(weight=weight_val)

            sent_msg = await message.answer("Теперь давайте запишем вашу почту, для дальнейшей связи: ")
            await state.update_data(last_msg_id=sent_msg.message_id)

            await state.set_state(RegistrationUsers.mail)
        else:
            await message.answer("Вес должен быть от 40 до 300 кг. Введи корректный вес:")
    
    except ValueError:
        await message.answer(
            "Извини, но это не похоже на число. 🧐\n"
            "Пожалуйста, введи только цифры (например: 75)")



async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
@router.message(RegistrationUsers.mail)
async def process_mail(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return
        
        mail_str = str(message.text)
        if validate_email(mail_str):
            await state.update_data(mail=mail_str)
            
            user_data = await state.get_data()

            async with async_session() as session:
                    new_user = User(
                        telegram_id=message.from_user.id,
                        tg_username=message.from_user.username,
                        fio=user_data.get("fio"),
                        age=user_data.get("age"),
                        height=user_data.get("height"),
                        weight=user_data.get("weight"),
                        mail=user_data.get("mail")
                    )
            
            session.add(new_user)
            await session.commit()
            await state.clear()

            await message.answer("Какой у вас запрос?",
            reply_markup=get_finish_keyboard()
            )
        else:
            await message.answer("Некорректный email!")
    except ValueError:
        await message.answer("Неккоректный email! Пример: test@mail.ru")
        return
    
    except Exception as e:
        await session.rollback()
        await message.answer("❌ Ошибка при финальном сохранении.")
        print(f"Ошибка БД: {e}")







@router.callback_query(F.data == "gets_improve")
async def start_survey_improve(callback: types.CallbackQuery, state: FSMContext):
    if not await clean_chat(callback, state):
            return

    await callback.message.delete()
    async with async_session() as session:
        
        statement = select(User).where(User.telegram_id == callback.from_user.id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            
            user.improve_ment = True
            
            
            await session.commit()
    await callback.answer()

    sent_msg = await callback.message.answer("Что вас беспокоит? Опишите свою проблему подробно.")
    await state.update_data(last_msg_id=sent_msg.message_id)

    await state.set_state(RegistationImprovement.problem)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
@router.message(RegistationImprovement.problem)
async def process_problem(message: types.Message, state: FSMContext):
        if not await clean_chat(message, state):
            return

        problem_str  = str(message.text)
        await state.update_data(problem=problem_str)
        
        user_data = await state.get_data()
        async with async_session() as session:

            new_user_improve = Improvement(
                users_tg=message.from_user.id, 
                tg_username=message.from_user.username, 
                improve_ment=user_data.get("improve_ment", True), 
                problem=message.text 
            )
        
            
        session.add(new_user_improve)
        await session.commit()
        await state.clear()
        await message.answer("Отлично! Ваша анкета составлена.")
        await send_profile_info(message, message.from_user.id)








@router.callback_query(F.data == "gets_loss")
async def start_survey_loss(callback: types.CallbackQuery, state: FSMContext):
    async with async_session() as session:
        await callback.message.delete()

        statement = select(User).where(User.telegram_id == callback.from_user.id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            
            user.weight_loss = True
            
            
            await session.commit()
    try:
        await callback.answer()
    except Exception as e:
        print(f"Callback answer failed (probably old query): {e}")

    sent_msg = await callback.message.answer("Отлично, на сколько килограмм вы бы хотели похудеть?")
    await state.update_data(last_msg_id=sent_msg.message_id)

    await state.set_state(RegistrationWeightloss.how_kg)

@router.message(RegistrationWeightloss.how_kg)
async def process_how_kg_loss(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return

        how_kg_loss  = int(message.text)
        if how_kg_loss > 0 and how_kg_loss <= 10:
            clean_chat(message, state)

            await state.update_data(how_kg=how_kg_loss)

            sent_msg = await message.answer("Это отличная цель! Теперь напишите мне сколько у вас приемов пищи в день?")
            await state.update_data(last_msg_id=sent_msg.message_id)

            await state.set_state(RegistrationWeightloss.how_eat_loss)
        else:
            await message.answer("Давайте пока начнем от малого к большому, напишите число от 1 до 10.")

    except ValueError:
        await message.answer(
            "Это не похоже на число, пожалуйста введите именно число! Например: 5")
        
@router.message(RegistrationWeightloss.how_eat_loss)
async def process_how_eat_loss(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return
        
        how_eat_loss  = int(message.text)
        if how_eat_loss > 1 and how_eat_loss <= 9:
            clean_chat(message, state)

            await state.update_data(how_eat=how_eat_loss)
            
            sent_msg = await message.answer("Понял, давайте теперь определимся с вашим уровнем физической активности в неделю. (Если ее нет - 0)")
            await state.update_data(last_msg_id=sent_msg.message_id)
            
            await state.set_state(RegistrationWeightloss.how_active_loss)
        else:
            await message.answer("Возможно вы ошиблись, напишите сколько у вас приемов пищи в день. (от 1 до 9)")


    except ValueError:
        await message.answer(
            "Это не похоже на число, пожалуйста введите именно число! Например: 3")
        
@router.message(RegistrationWeightloss.how_active_loss)
async def process_how_active_loss(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return

        how_active_week  = int(message.text)
        if how_active_week >= 0 and how_active_week <= 7:
            clean_chat(message, state)
            await state.update_data(how_active=how_active_week)

            await message.answer("Записал. Теперь выберите сколько вы пьете воды в день?",
                                reply_markup=how_water_keyboard())
            await state.set_state(RegistrationWeightloss.how_water_loss)
        else:
            await message.answer("Похоже вы где-то ошиблись, напиште свою активность в неделю. (от 0 до 7)")

    except ValueError:
        await message.answer(
            "Это не похоже на число, пожалуйста введите именно число! Например: 2")

@router.callback_query (RegistrationWeightloss.how_water_loss)
async def process_how_water_loss(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if not await clean_chat(callback, state):
            return


    WATER_MAP = {
    "no_water": "Не люблю пить воду",
    "mb_water": "Иногда пью",
    "like_water": "Пью и контролирую"
    }
    choice = WATER_MAP.get(callback.data)
    if not choice:
        await callback.answer("Неизвестный вариант", show_alert=True)
        return
        
    await state.update_data(how_water=choice)
    
    sent_msg = await callback.message.answer("Принял. А можете описать свой режим сна? (Например: нет режима, ложусь до 23)")
    await state.update_data(last_msg_id=sent_msg.message_id)

    await state.set_state(RegistrationWeightloss.how_sleep_loss)

@router.message(RegistrationWeightloss.how_sleep_loss)
async def process_how_sleep_loss(message: types.Message, state: FSMContext):
        if not await clean_chat(message, state):
                return
        how_sleep_str  = str(message.text)
        await state.update_data(how_sleep=how_sleep_str)
        
        user_data = await state.get_data()
        async with async_session() as session:

            new_user_loss = Weightloss(
                users_tg=message.from_user.id, 
                tg_username=message.from_user.username, 
                weight_loss=user_data.get("weight_loss", True), 
                how_kg=user_data.get("how_kg"),
                how_eat=user_data.get("how_eat"),
                how_active=user_data.get("how_active"),
                how_water=user_data.get("how_water"),
                how_sleep=user_data.get("how_sleep")
            )
        
            
        session.add(new_user_loss)
        await session.commit()
        await state.clear()
        await message.answer("Отлично, ваша анкета составлена!")
        await send_profile_info(message, message.from_user.id)






@router.callback_query(F.data == "gets_mode")
async def start_survey_mode(callback: types.CallbackQuery, state: FSMContext):
    async with async_session() as session:
        await callback.message.delete()

        statement = select(User).where(User.telegram_id == callback.from_user.id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            
            user.mode = True
            
            await session.commit()
    await callback.answer()

    await callback.message.answer("Отлично. Давайте определимся есть ли у вас лишний вес?",
                                 reply_markup=yes_or_not_keyboard())

    await state.set_state(RegistationMode.have_kg)

@router.callback_query(RegistationMode.have_kg)
async def process_have_kg(callback: types.CallbackQuery, state: FSMContext):
    
    if not await clean_chat(callback, state):
            return
    
    await callback.message.delete()
    YES_OR_NOT_MAP = {
        "input_yes": "Да",
        "input_no": "Нет"
    }
    choice = YES_OR_NOT_MAP.get(callback.data)
    if not choice:
        await callback.answer("Неизвестный вариант", show_alert=True)
        return
        
    await state.update_data(have_kg=choice)

    sent_msg = await callback.message.answer("Теперь напишите мне сколько у вас приемов пищи в день? Например: 4")
    await state.update_data(last_msg_id=sent_msg.message_id)
    
    await state.set_state(RegistationMode.how_eat_mode)
    

@router.message(RegistationMode.how_eat_mode)
async def process_how_eat_mode(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return
        
        how_eat_loss  = int(message.text)
        if how_eat_loss > 1 and how_eat_loss <= 9:
            clean_chat(message, state)

            await state.update_data(how_eat=how_eat_loss)
            
            sent_msg = await message.answer("Понял, давайте теперь определимся с вашим уровнем физической активности в неделю. (Если ее нет - 0)")
            await state.update_data(last_msg_id=sent_msg.message_id)
            
            await state.set_state(RegistationMode.how_active_mode)
        else:
            await message.answer("Возможно вы ошиблись, напишите сколько у вас приемов пищи в день. (от 1 до 9)")

    except ValueError:
        await message.answer(
            "Это не похоже на число, пожалуйста введите именно число! Например: 3")
        
@router.message(RegistationMode.how_active_mode)
async def process_how_active_mode(message: types.Message, state: FSMContext):
    try:
        if not await clean_chat(message, state):
            return

        how_active_week  = int(message.text)
        if how_active_week >= 0 and how_active_week <= 7:
            clean_chat(message, state)
            await state.update_data(how_active=how_active_week)

            await message.answer("Записал. Теперь выберите сколько вы пьете воды в день?",
                                reply_markup=how_water_keyboard())
            await state.set_state(RegistationMode.how_water_mode)
        else:
            await message.answer("Похоже вы где-то ошиблись, напиште свою активность в неделю. (от 0 до 7)")

    except ValueError:
        await message.answer(
            "Это не похоже на число, пожалуйста введите именно число! Например: 2")

@router.callback_query (RegistationMode.how_water_mode)
async def process_how_water_mode(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if not await clean_chat(callback, state):
            return

    WATER_MAP = {
    "no_water": "Не люблю пить воду",
    "mb_water": "Иногда пью",
    "like_water": "Пью и контролирую"
    }
    choice = WATER_MAP.get(callback.data)
    if not choice:
        await callback.answer("Неизвестный вариант", show_alert=True)
        return
        
    await state.update_data(how_water=choice)

    sent_msg = await callback.message.answer("Принял. А можете описать словами свой режим сна? (Например: нет режима, ложусь до 23)")
    await state.update_data(last_msg_id=sent_msg.message_id)

    await state.set_state(RegistationMode.how_sleep_mode)

@router.message(RegistationMode.how_sleep_mode)
async def process_how_sleep_mode(message: types.Message, state: FSMContext):
        if not await clean_chat(message, state):
            return
            
        how_sleep_str  = str(message.text)
        await state.update_data(how_sleep=how_sleep_str)
        
        user_data = await state.get_data()
        async with async_session() as session:

            new_user_mode = Modes(
                users_tg=message.from_user.id, 
                tg_username=message.from_user.username, 
                mode=user_data.get("mode", True), 
                have_kg=user_data.get("have_kg"),
                how_eat=user_data.get("how_eat"),
                how_active=user_data.get("how_active"),
                how_water=user_data.get("how_water"),
                how_sleep=user_data.get("how_sleep")
            )
        
            
        session.add(new_user_mode)
        await session.commit()
        await state.clear()
        await message.answer("Отлично, ваша анкета составлена!")
        await send_profile_info(message, message.from_user.id)





    
        


    
        