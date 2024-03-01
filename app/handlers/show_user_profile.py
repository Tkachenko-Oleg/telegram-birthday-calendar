from aiogram.types import Message
from aiogram.filters import Command

from main import dp, tools, datasource, phrases, panels


@dp.message(Command('my_profile'))
async def show_user_profile_command_handler(message: Message):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        postgres_data = datasource.user_profile(tg_id=message.from_user.id)
        data = tools.parse_postgres(postgres_data)
        text = f"{phrases['fields']['nick'][lang]}: {data.get('nick')}\n" \
               f"{phrases['fields']['name'][lang]}: {data.get('name')}\n" \
               f"{phrases['fields']['birthday'][lang]}: {data.get('birth')}\n" \
               f"{phrases['fields']['phone'][lang]}: {data.get('phone')}\n" \
               f"{phrases['fields']['language'][lang]}: {data.get('lang')}"

        await message.answer(text=text, reply_markup=panels.commands_panel())
    else:
        await message.answer("You are not registered")
