from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource, phrases, panels, tools


@dp.message(Command('birthday_list'))
async def show_user_birthday_list_command_handler(message: Message):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    if usr_id:
        lang = datasource.get_lang(usr_id)
        friend_id_list = datasource.get_relationship_ids(usr_id)
        text = str()
        if friend_id_list:
            for friend_id in friend_id_list:
                postgres_data = datasource.get_birthday(friend_id)
                friend_data = tools.format_info_about_friend(postgres_data)
                text += friend_data
            await message.answer(text)
        else:
            text = phrases['phrases']['emptyBirthdayList'][lang]
            await message.answer(text=text, reply_markup=panels.commands_panel())
    else:
        await message.answer("You are not registered")
