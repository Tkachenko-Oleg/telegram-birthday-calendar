from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.main import dp, datasource, phrases
from app.bot.services.tools import Tools
from app.bot.states.profile import ProfileState
from app.bot.keyboards import days_keyboard, language_keyboard, months_keyboard, \
                              options_keyboard, remove_keyboard, main_keyboard


@dp.message(ProfileState.profile_is_active, F.text.startswith('🛠'))
async def change_user_profile_command_handler(message: Message, state: FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['changeSetting'][lang]
        await state.set_state(ProfileState.choice)
        await message.answer(text=text, reply_markup=options_keyboard(phrases, lang))
    else:
        await message.answer("You are not registered")


@dp.message(ProfileState.choice)
async def identify_change(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    if message.text == phrases['phrases']['Back'][lang]:
        text = phrases['main'][lang]
        await message.answer(text=text, reply_markup=main_keyboard())
        await state.clear()

    elif message.text == phrases['phrases']['changeLanguage'][lang]:
        text = phrases['phrases']['selectLanguage'][lang]
        await message.answer(text=text, reply_markup=language_keyboard())
        await state.set_state(ProfileState.change_language)

    elif message.text == phrases['phrases']['changeName'][lang]:
        text = phrases['phrases']['enterName'][lang]
        await message.answer(text=text, reply_markup=remove_keyboard())
        await state.set_state(ProfileState.change_name)

    elif message.text == phrases['phrases']['changeBirthday'][lang]:
        text = phrases['phrases']['selectMonth'][lang]
        await message.answer(text=text, reply_markup=months_keyboard(phrases, lang))
        await state.set_state(ProfileState.change_birth_month)

    else:
        await message.delete()


@dp.message(ProfileState.change_language)
async def change_language(message: Message, state: FSMContext):
    is_lang_selected = True
    curr_lang = 'En'

    if message.text == "Русский 🇷🇺":
        curr_lang = 'Ru'
    elif message.text == "English 🇬🇧":
        curr_lang = 'En'
    else:
        is_lang_selected = False

    if is_lang_selected:
        text = phrases['phrases']['updateProfile'][curr_lang]
        datasource.change_language(tg_id=message.from_user.id, lang=curr_lang)
        await message.answer(text=text, reply_markup=main_keyboard())
        await state.clear()
    else:
        await message.delete()


@dp.message(ProfileState.change_name)
async def change_name(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    text = Tools.is_correct_name_message(message.text, phrases, lang)
    is_name_changed = False

    if text == "correct message":
        text = phrases['phrases']['updateProfile'][lang]
        is_name_changed = True
    await message.answer(text=text, reply_markup=main_keyboard())
    if is_name_changed:
        datasource.change_name(tg_id=message.from_user.id, name=message.text)
        await state.clear()


@dp.message(ProfileState.change_birth_month)
async def change_month(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    month_number = Tools.get_month_number(message.text, lang)

    if month_number:
        text = phrases['phrases']['selectDay'][lang]
        await state.update_data(month=month_number)
        await message.answer(text=text, reply_markup=days_keyboard(month_number))
        await state.set_state(ProfileState.change_birth_day)
    else:
        await message.delete()


@dp.message(ProfileState.change_birth_day)
async def change_day(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    state_data = await state.get_data()
    month_number = state_data.get('month')
    user_day = Tools.correct_day(message.text, month_number)

    if user_day:
        datasource.change_birthday(tg_id=message.from_user.id, birth_month=month_number, birthday=user_day)
        text = phrases['phrases']['updateProfile'][lang]
        await message.answer(text=text, reply_markup=main_keyboard())
        await state.clear()
    else:
        await message.delete()
