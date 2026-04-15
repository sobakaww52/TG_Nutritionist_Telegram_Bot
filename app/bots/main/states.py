from aiogram.fsm.state import State, StatesGroup

class RegistrationUsers(StatesGroup):
    first_name = State()
    age = State()
    height = State()
    weight = State()