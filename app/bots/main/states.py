from aiogram.fsm.state import State, StatesGroup

class RegistrationUsers(StatesGroup):
    age = State()
    height = State()
    weight = State()