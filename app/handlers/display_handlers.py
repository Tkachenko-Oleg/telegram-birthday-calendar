from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource

@dp.message(Command('show_all_birthdays'))
async def show_all_birthdays_command_handler(message: Message):
    await message.answer(datasource.get_all_birthdays(str(message.from_user.id)))


@dp.message(Command('show_birthdays_today'))
async def show_birthdays_today_command_handler(message: Message):
    await message.answer(datasource.get_today_birthdays(str(message.from_user.id)))
