from aiogram.fsm.state import State, StatesGroup

class RegistrationState(StatesGroup):
    tg_id_state = State()
    language_state = State()
    phone_number_state = State()
    nickname_state = State()
    username_state = State()
    month_state = State()
    day_state = State()
