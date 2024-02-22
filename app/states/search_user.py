from aiogram.fsm.state import State, StatesGroup

class FormSearchUser(StatesGroup):
    contact_id = State()
    user_id = State()
