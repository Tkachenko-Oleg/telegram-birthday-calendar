from aiogram.fsm.state import State, StatesGroup

class FormChangeUserProfile(StatesGroup):
    name = State()
    month_of_birth = State()
    day_of_birth = State()
