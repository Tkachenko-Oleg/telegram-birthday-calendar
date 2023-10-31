from aiogram.types import Message
from aiogram.filters import Command

from .bot_command_logic import BotCommandLogic

from main import dp
from services import Data
DATA = Data.data


@dp.message(Command('show_all_birthdays'))
async def show_all_birthdays_command_handler(message: Message):
    await message.answer(BotCommandLogic.get_all_birthdays(DATA, str(message.from_user.id)))


@dp.message(Command('show_birthdays_today'))
async def show_birthdays_today_command_handler(message: Message):
    await message.answer(BotCommandLogic.get_today_birthdays(DATA, str(message.from_user.id)))
