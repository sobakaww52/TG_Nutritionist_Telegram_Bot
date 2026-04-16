from aiogram.fsm.state import State, StatesGroup

class RegistrationUsers(StatesGroup):
    fio = State()
    age = State()
    height = State()
    weight = State()
    mail = State()

class RegistrationWeightless(StatesGroup):
    how_kg = State()
    how_eat = State()
    how_active = State()
    how_water = State()
    how_sleep = State()

class RegistationImprovement(StatesGroup):
    problem = State()

class RegistationMode(StatesGroup):
    have_kg = State()
    how_eat = State()
    how_active = State()
    how_water = State()
    how_sleep = State()