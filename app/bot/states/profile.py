from aiogram.fsm.state import State, StatesGroup

class ProfileState(StatesGroup):
    profile_is_active = State()

    choice = State()
    change_language = State()
    change_name = State()
    change_birth_month = State()
    change_birth_day = State()

    delete_state = State()
