from aiogram.fsm.state import State, StatesGroup

class FormSearchUser(StatesGroup):
    nickname = State()
    phone_number = State()
    user_id_to_add = State()
