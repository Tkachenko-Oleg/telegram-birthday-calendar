from aiogram.fsm.state import State, StatesGroup

class FormRegistration(StatesGroup):
    tg_id = State()
    language = State()
    phone_number = State()
    nickname = State()
    name = State()
    birth_month = State()
    birthday = State()
