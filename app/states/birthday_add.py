from aiogram.fsm.state import State, StatesGroup


class FormAddNewBirthday(StatesGroup):
    name = State()
    year_of_birth = State()
    month_of_birth = State()
    day_of_birth = State()
