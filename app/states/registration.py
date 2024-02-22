from aiogram.fsm.state import State, StatesGroup

class FormRegistration(StatesGroup):
    tg_id = State()
    username = State()
    nickname = State()
    phone_number = State()
    language = State()
    month_of_birth = State()
    day_of_birth = State()
