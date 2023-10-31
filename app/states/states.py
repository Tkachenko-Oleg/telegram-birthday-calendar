from aiogram.fsm.state import State, StatesGroup


class FormAddNewBirthday(StatesGroup):
    name = State()
    year = State()
    month = State()
    day = State()
