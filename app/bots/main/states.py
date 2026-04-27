from aiogram.fsm.state import State, StatesGroup

class RegistrationUsers(StatesGroup):
    fio = State()
    age = State()
    height = State()
    weight = State()
    mail = State()

class RegistrationWeightloss(StatesGroup):
    how_kg = State()
    how_eat_loss = State()
    how_active_loss = State()
    how_water_loss = State()
    how_sleep_loss = State()

class RegistationImprovement(StatesGroup):
    problem = State()

class RegistationMode(StatesGroup):
    have_kg = State()
    how_eat_mode = State()
    how_active_mode = State()
    how_water_mode = State()
    how_sleep_mode = State()