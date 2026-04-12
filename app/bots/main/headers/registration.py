from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.bots.main.states import RegistrationUsers
from app.models.users import User
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database import engine

router = Router()

@router.callback_query(F.data == "start_registration")
async def start_survey(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваш возраст:")
    await state.set_state(RegistrationUsers.age)

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

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
@router.message(RegistrationUsers.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight_val = float(message.text.replace(",", "."))

        await state.update_data(weight=weight_val)
        

    
        user_data = await state.get_data()
    
        async with async_session() as session:

            new_user = User(
                telegram_id=message.from_user.id,
                tg_username=message.from_user.username,
                age=user_data.get("age"),
                height=user_data.get("height"),
                weight=user_data.get("weight"),
            )
            
            session.add(new_user)
            await session.commit()
        
        await state.clear() 
        await message.answer("✅ Анкета успешно сохранена! Данные уже в базе.")
    except ValueError:
        await message.answer("Пожалуйста, введи вес цифрами (например: 75.5)")
        return 

    except Exception as e:
        await session.rollback()
        await message.answer("❌ Ошибка при финальном сохранении.")
        print(f"Ошибка БД: {e}")
        