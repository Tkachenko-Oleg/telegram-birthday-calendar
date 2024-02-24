from aiogram.types import Message
from aiogram.filters import Command

from main import dp, datasource, phrases, panels


@dp.message(Command('help'))
async def help_handler(message: Message):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    if usr_id:
        lang = datasource.get_lang(usr_id)
        text = f"{phrases['helpText']['showProfile'][lang]}\n\n" \
               f"{phrases['helpText']['changeProfile'][lang]}\n\n" \
               f"{phrases['helpText']['deleteProfile'][lang]}\n\n" \
               f"{phrases['helpText']['searchProfile'][lang]}\n\n" \
               f"{phrases['helpText']['showBirthdayList'][lang]}"
        await message.answer(text=text, reply_markup=panels.commands_panel())
    else:
        await message.answer("You are not registered")
