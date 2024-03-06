from aiogram.types import Message
from aiogram.filters import Command

from main import dp, tools, datasource, phrases, panels


@dp.message(Command('help'))
async def help_handler(message: Message):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = tools.create_help_text(phrases, lang)
        await message.answer(text=text, reply_markup=panels.commands_panel())
    else:
        await message.answer("You are not registered")
