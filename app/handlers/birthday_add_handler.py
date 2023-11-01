from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# from app.services.bot_command_logic import BotCommandLogic

from states import *
from main import dp
from services import Data, BotCommandLogic
DATA = Data.data


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
    if BotCommandLogic.check_correct_data(year=dict(await state.get_data()).get('year'),
                                          month=message.text):
        await state.update_data(month=message.text)
        await state.set_state(FormAddNewBirthday.day)
        await message.answer("Input day birthday: ")
    else:
        await message.answer("The month is incorrect!")


@dp.message(FormAddNewBirthday.day)
async def process_birthday_day_add(message: Message, state: FSMContext):
    if BotCommandLogic.check_correct_data(year=dict(await state.get_data()).get('year'),
                                          month=dict(await state.get_data()).get('month'),
                                          day=message.text):
        await state.update_data(day=message.text)
        await message.answer(BotCommandLogic.add_new_birthday(DATA, await state.get_data(), str(message.from_user.id)))
        await state.clear()
    else:
        await message.answer("The day is incorrect!")
