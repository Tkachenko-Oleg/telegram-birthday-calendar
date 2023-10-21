from aiogram import Dispatcher
from datetime import datetime
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from data_list import Data
DATA = Data.data

dp = Dispatcher()

# commands:
# start
# help
# change language
# add birthday
# delete birthday
# change birthday
# show all birthdays
# show birthdays this week


class Form(StatesGroup):
    name = State()
    year = State()
    month = State()
    day = State()


@dp.message(Command('start'))
async def start_command_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!\nBot is running")


@dp.message(Command('add_birthday'))
async def add_birthday_command_handler(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Input name user: ")


@dp.message(Form.name)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.year)
    await message.answer("Input year birthday: ")


@dp.message(Form.year)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(Form.month)
    await message.answer("Input month birthday: ")


@dp.message(Form.month)
async def process_name_add(message: Message, state: FSMContext):
    await state.update_data(month=message.text)
    await state.set_state(Form.day)
    await message.answer("Input day birthday: ")


@dp.message(Form.day)
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


@dp.message(Command('show_all_birthdays'))
async def show_all_birthdays_command_handler(message: Message):
    answer_string = str()
    for i in DATA:
        answer_string += (f"{DATA[i]['name']}: "
                          f"{DATA[i]['birthday']['year']}."
                          f"{DATA[i]['birthday']['month']}."
                          f"{DATA[i]['birthday']['day']}\n")
    await message.answer(answer_string)


@dp.message(Command('show_birthdays_today'))
async def show_birthdays_today_command_handler(message: Message):
    answer_string = str()
    for i in DATA:
        i_data = f"{DATA[i]['birthday'].get('year')}.{DATA[i]['birthday'].get('month')}.{DATA[i]['birthday'].get('day')}"
        if i_data == str(datetime.date(datetime.now())).replace('-', '.'):
            answer_string += (f"{DATA[i]['name']}: "
                              f"{DATA[i]['birthday']['year']}."
                              f"{DATA[i]['birthday']['month']}."
                              f"{DATA[i]['birthday']['day']}\n")
    if answer_string:
        await message.answer(f"Today birthdays:\n{answer_string}")
    else:
        await message.answer("Today birthdays is not found")
