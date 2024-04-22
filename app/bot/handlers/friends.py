from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.main import dp, datasource, phrases
from app.bot.services.tools import Tools
from app.bot.states.friends import FriendsState
from app.bot.keyboards import friend_keyboard, main_keyboard


@dp.message(Command('friends'))
async def show_user_birthday_list_command_handler(message: Message, state: FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        list_of_birthdays = datasource.get_friend_birthdays(message.from_user.id)
        if list_of_birthdays:
            text = Tools.convert_postgres_birthdays_list_to_string(list_of_birthdays, phrases, lang)
        else:
            text = phrases['phrases']['emptyBirthdayList'][lang]
        await message.answer(text=text, reply_markup=friend_keyboard(phrases, lang))
        await state.set_state(FriendsState.friends_is_active)
    else:
        await message.answer("You are not registered")


@dp.message(FriendsState.friends_is_active, ~F.text.startswith('➕'), ~F.text.startswith('ℹ️'))
async def clear_friends_state(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    await message.answer(text=phrases['main'][lang], reply_markup=main_keyboard())
    await state.clear()
