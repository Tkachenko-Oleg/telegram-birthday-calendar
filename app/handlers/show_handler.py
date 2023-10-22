from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.main import dp
from app.services import Data
DATA = Data.data


class FormAddNewBirthday(StatesGroup):
    name = State()
    year = State()
    month = State()
    day = State()


@dp.message(Command('add_birthday'))
async def add_birthday_command_handler(message: Message, state: FSMContext):
    await state.set_state(FormAddNewBirthday.name)
    await message.answer("Input name user: ")


@dp.message(FormAddNewBirthday.name)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormAddNewBirthday.year)
    await message.answer("Input year birthday: ")


@dp.message(FormAddNewBirthday.year)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(FormAddNewBirthday.month)
    await message.answer("Input month birthday: ")


@dp.message(FormAddNewBirthday.month)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(month=message.text)
    await state.set_state(FormAddNewBirthday.day)
    await message.answer("Input day birthday: ")


@dp.message(FormAddNewBirthday.day)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    new_data = await state.get_data()
    new_key = len(DATA)
    new_value = {'name': new_data.get('name'),
                 'birthday': {'year': new_data.get('year'),
                              'month': new_data.get('month'),
                              'day': new_data.get('day')}}
    DATA.update({new_key: new_value})
    await state.clear()
    await message.answer(f"Your new data:\n{new_data.get('name')}: "
                         f"{new_data.get('year')}.{new_data.get('month')}.{new_data.get('day')}")

