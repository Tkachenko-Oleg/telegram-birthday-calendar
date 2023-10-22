from datetime import datetime
from aiogram.types import Message
from aiogram.filters import Command

from .bot_command_logic import BotCommandLogic

from app.main import dp
from app.services import Data
DATA = Data.data


@dp.message(Command('start'))
async def start_command_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!\nBot is running")


@dp.message(Command('show_all_birthdays'))
async def show_all_birthdays_command_handler(message: Message):
    # answer_string = str()
    # for i in DATA:
    #     answer_string += (f"{DATA[i]['name']}: "
    #                       f"{DATA[i]['birthday']['year']}."
    #                       f"{DATA[i]['birthday']['month']}."
    #                       f"{DATA[i]['birthday']['day']}\n")
    await message.answer(BotCommandLogic.get_all_birthdays(..., DATA))


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
