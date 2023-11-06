from aiogram.fsm.state import State, StatesGroup

class FormRegistration(StatesGroup):
    language = State()
    phone_number = State()
    nickname = State()
    name = State()
    year_of_birth = State()
    month_of_birth = State()
    day_of_birth = State()
