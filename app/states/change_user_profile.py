from aiogram.fsm.state import State, StatesGroup

class FormChangeUserProfile(StatesGroup):
    choice = State()
    language = State()
    name = State()
    birth_month = State()
    birthday = State()
