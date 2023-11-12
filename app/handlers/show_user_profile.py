from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource


@dp.message(Command('show_my_profile'))
async def show_user_profile_command_handler(message: Message):
    user_id = message.from_user.id
    is_exist_user_profile = datasource.check_exist_user(user_id)
    if is_exist_user_profile:
        await message.answer(datasource.show_user_profile(user_id))
    else:
        await message.answer("You are not registered")
