from aiogram.types import Message
from aiogram.filters import Command

from main import dp, tools, datasource, phrases, panels


@dp.message(Command('birthday_list'))
async def show_user_birthday_list_command_handler(message: Message):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        usr_id = datasource.get_id(tg_id=message.from_user.id)
        friend_id_list = datasource.get_relationship_ids(usr_id=usr_id)
        if friend_id_list:
            text = str()
            for friend_id in friend_id_list:
                postgres_data = datasource.get_birthday(usr_id=friend_id)
                friend_data = tools.format_info_about_friend(postgres_data)
                text += friend_data
        else:
            text = phrases['phrases']['emptyBirthdayList'][lang]

        await message.answer(text=text, reply_markup=panels.commands_panel())

    else:
        await message.answer("You are not registered")
