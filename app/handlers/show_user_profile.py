from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource


@dp.message(Command('show_my_profile'))
async def show_user_profile_command_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(str(message.from_user.id))
    if is_exist_user_profile:
        await message.answer(datasource.show_user_profile(str(message.from_user.id)))
    else:
        await message.answer("You are not registered")
