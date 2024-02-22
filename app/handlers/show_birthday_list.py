from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource


@dp.message(Command('show_my_birthday_list'))
async def show_user_birthday_list_command_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(str(message.from_user.id))
    if is_exist_user_profile:
        user_id = datasource.get_id_user(str(message.from_user.id))
        ids_list = datasource.show_list_of_birthdays(user_id)
        answer = str()
        if ids_list:
            for friend_id in ids_list:
                answer += f"{datasource.get_info_about_birthday(friend_id)}\n"
            await message.answer(answer)
        else:
            await message.answer("Your birthday list is empty")
    else:
        await message.answer("You are not registered")
