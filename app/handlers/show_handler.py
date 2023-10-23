from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .bot_command_logic import BotCommandLogic

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
async def process_birthday_name_add(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormAddNewBirthday.year)
    await message.answer("Input year birthday: ")


@dp.message(FormAddNewBirthday.year)
async def process_birthday_year_add(message: Message, state: FSMContext):
    if BotCommandLogic.check_correct_data(year=message.text):
        await state.update_data(year=message.text)
        await state.set_state(FormAddNewBirthday.month)
        await message.answer("Input month birthday: ")
    else:
        await message.answer("The year is incorrect!")


@dp.message(FormAddNewBirthday.month)
async def process_birthday_month_add(message: Message, state: FSMContext):
    tmp_date = await state.get_data()
    if BotCommandLogic.check_correct_data(year=tmp_date['year'], month=message.text):
        await state.update_data(month=message.text)
        await state.set_state(FormAddNewBirthday.day)
        await message.answer("Input day birthday: ")
    else:
        await message.answer("The month is incorrect!")


@dp.message(FormAddNewBirthday.day)
async def process_birthday_day_add(message: Message, state: FSMContext):
    tmp_date = await state.get_data()
    if BotCommandLogic.check_correct_data(year=tmp_date['year'], month=tmp_date['month'], day=message.text):
        await state.update_data(day=message.text)
        await message.answer(BotCommandLogic.add_new_birthday(DATA, await state.get_data()))
        await state.clear()
    else:
        await message.answer("The day is incorrect!")
