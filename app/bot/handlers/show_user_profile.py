from aiogram.types import Message
from aiogram.filters import Command

from main import dp, tools, datasource, phrases, panels


@dp.message(Command('my_profile'))
async def show_user_profile_command_handler(message: Message):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        postgres_data = datasource.user_profile(tg_id=message.from_user.id)
        text = tools.parse_postgres(postgres_data, phrases, lang)
        await message.answer(text=text, reply_markup=panels.commands_panel())
    else:
        await message.answer("You are not registered")
