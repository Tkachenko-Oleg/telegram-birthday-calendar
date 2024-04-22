from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.main import dp, datasource, phrases
from app.bot.services.tools import Tools
from app.bot.states.profile import ProfileState
from app.bot.keyboards import profile, main_keyboard


@dp.message(Command('profile'))
async def show_user_profile_command_handler(message: Message, state: FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        postgres_data = datasource.user_profile(tg_id=message.from_user.id)
        text = Tools.parse_postgres(postgres_data, phrases, lang)
        await message.answer(text=text, reply_markup=profile(phrases, lang))
        await state.set_state(ProfileState.profile_is_active)
    else:
        await message.answer("You are not registered")


@dp.message(ProfileState.profile_is_active, ~F.text.startswith('🗑'), ~F.text.startswith('🛠'))
async def clear_profile_state(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    text = phrases['main'][lang]
    await message.answer(text=text, reply_markup=main_keyboard())
    await state.clear()
