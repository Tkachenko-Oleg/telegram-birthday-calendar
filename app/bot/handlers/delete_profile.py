from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.main import dp, datasource, phrases
from app.bot.states.profile import ProfileState
from app.bot.keyboards import remove_keyboard, delete_profile_keyboard, main_keyboard


@dp.message(ProfileState.profile_is_active, F.text.startswith('🗑'))
async def delete_user_profile_command_handler(message: Message, state: FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['confirmation'][lang]
        await message.answer(text=text, reply_markup=delete_profile_keyboard(phrases, lang))
        await state.set_state(ProfileState.delete_state)
    else:
        await message.answer("You are not registered")


@dp.message(ProfileState.delete_state)
async def delete_user_profile(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    if message.text == phrases['phrases']['questDelProfile'][lang]:
        text = phrases['phrases']['messageDelProfile'][lang]
        datasource.delete_profile(tg_id=message.from_user.id)
        keyboard = remove_keyboard()
    else:
        await message.answer(text=phrases['phrases']['messageNotDelProfile'][lang])
        text = phrases['main'][lang]
        keyboard = main_keyboard()

    await message.answer(text=text, reply_markup=keyboard)
    await state.clear()
