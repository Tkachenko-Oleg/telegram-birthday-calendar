from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource


@dp.message(Command('help'))
async def help_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(str(message.from_user.id))
    if is_exist_user_profile:
        await message.answer("Commands:\n"
                             "/show_my_profile\n"
                             "/change_my_profile\n"
                             "/delete_my_profile\n"
                             "/search_user\n"
                             "/show_my_birthday_list - not working")
    else:
        await message.answer("You are not registered")
