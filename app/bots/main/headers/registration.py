from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlmodel import select

from app.bots.main.states import RegistrationUsers, RegistationImprovement, RegistationMode, RegistrationWeightless
from app.models.users import User, Improvement, Weightloss, Modes
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database import engine

from app.bots.main.headers.email_validate import validate_email
from app.bots.main.keyboards.inlines import get_finish_keyboard

router = Router()

@router.callback_query(F.data == "start_registration")
async def start_survey_first(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваше ФИО:")
    await state.set_state(RegistrationUsers.fio)

@router.message(RegistrationUsers.fio)
async def process_age(message: types.Message, state: FSMContext):
    try:
        fio_str  = str(message.text)
        await state.update_data(fio=fio_str)
        await message.answer("Принято, теперь напиши мне свой возраст: ")
        await state.set_state(RegistrationUsers.age)


    except ValueError:
        await message.answer(
            "Извини, введите корректное имя. 🧐 Например(Артем)\n")
        
@router.message(RegistrationUsers.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age_val = int(message.text)
        if 14 <= age_val <= 90:
            await state.update_data(age=age_val)
            await message.answer("Принято, теперь напиши мне свой рост(см): ")
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
        height_val = int(message.text)
        if 100 <= height_val <= 250:
            await state.update_data(height=height_val)
            await message.answer("Отлично, теперь напиши мне свой вес(кг): ")
            await state.set_state(RegistrationUsers.weight)
        else:
            await message.answer("Рост должен быть от 100 до 250 см. Введи корректный рост:")
    
    except ValueError:
        await message.answer(
            "Извини, но это не похоже на число. 🧐\n"
            "Пожалуйста, введи только цифры (например: 170)")
        
@router.message(RegistrationUsers.weight)
async def process_height(message: types.Message, state: FSMContext):
    try:
        weight_val = float(message.text.replace(",", "."))
        if 40<= weight_val <= 300:
            await state.update_data(weight=weight_val)
            await message.answer("Теперь давайте запишем вашу почту, для дальнейшей связи: ")
            await state.set_state(RegistrationUsers.mail)
        else:
            await message.answer("Вес должен быть от 40 до 300 кг. Введи корректный вес:")
    
    except ValueError:
        await message.answer(
            "Извини, но это не похоже на число. 🧐\n"
            "Пожалуйста, введи только цифры (например: 75)")



async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
@router.message(RegistrationUsers.mail)
async def process_weight(message: types.Message, state: FSMContext):
    try:
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
    async with async_session() as session:
        
        statement = select(User).where(User.telegram_id == callback.from_user.id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            
            user.weight_loss = True
            
            
            await session.commit()
    await callback.answer()
    await callback.message.answer("Что вас беспокоит? Опишите свою проблему подробно.")
    await state.set_state(RegistationImprovement.problem)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
@router.message(RegistationImprovement.problem)
async def process_age(message: types.Message, state: FSMContext):
        
        problem_str  = str(message.text)
        await state.update_data(problem=problem_str)
        
        user_data = await state.get_data()
        async with async_session() as session:
                    new_user_improve = Improvement(
                        users_tg=message.from_user.id,
                        problem=user_data.get("problem")
                    )
        
            
        session.add(new_user_improve)
        await session.commit()
        await state.clear()


    
        


    
        