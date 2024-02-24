from aiogram.fsm.state import State, StatesGroup

class FormSearchUser(StatesGroup):
    search_state = State()
    contact_id = State()
    nickname_state = State()
    add_state = State()
