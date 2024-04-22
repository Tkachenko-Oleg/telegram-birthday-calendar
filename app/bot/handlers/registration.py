from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.bot.main import dp, datasource, phrases
from app.bot.states.registration import RegistrationState
from app.bot.services.tools import Tools
from app.bot.keyboards import language_keyboard, main_keyboard, registration_keyboard,\
                              remove_keyboard, months_keyboard, days_keyboard


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not datasource.is_user_exist(tg_id=message.from_user.id):
        text = (f"{message.from_user.full_name} 👋\n\n"
                f"🇬🇧: Choose language\n"
                f"🇷🇺: Выберете язык")
        await message.answer(text=text, reply_markup=language_keyboard())
        await state.set_state(RegistrationState.language_state)
    else:
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['registrationIsAlreadyCompleted'][lang]
        await message.answer(text=text)
        menu = phrases['main'][lang]
        await message.answer(text=menu, reply_markup=main_keyboard())


@dp.message(RegistrationState.language_state)
async def enter_language(message: Message, state: FSMContext):
    is_lang_selected = True
    curr_lang = 'En'

    if message.text == "Русский 🇷🇺":
        curr_lang = 'Ru'
    elif message.text == "English 🇬🇧":
        curr_lang = 'En'
    else:
        is_lang_selected = False

    if is_lang_selected:
        text = phrases['phrases']['shareContactMessage'][curr_lang]
        await message.answer(text=text, reply_markup=registration_keyboard(phrases, curr_lang))
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(language=curr_lang)
        await state.set_state(RegistrationState.phone_number_state)
    else:
        await message.delete()


@dp.message(RegistrationState.phone_number_state)
async def enter_phone_number(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('language')
    if message.contact:
        text = phrases['phrases']['enterNickname'][lang]
        await message.answer(text=text, reply_markup=remove_keyboard())
        await state.update_data(phone_number=message.contact.phone_number)
        await state.set_state(RegistrationState.nickname_state)
    else:
        await message.delete()


@dp.message(RegistrationState.nickname_state)
async def enter_nickname(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('language')
    text = Tools.is_correct_name_message(message.text, phrases, lang)
    next_state = False

    if text == "correct message":
        if not datasource.is_nickname_exist(nickname=message.text):
            next_state = True
            text = phrases['phrases']['enterName'][lang]
        else:
            text = phrases['phrases']['nicknameExist'][lang]
    await message.answer(text=text)
    if next_state:
        await state.update_data(nickname=message.text)
        await state.set_state(RegistrationState.username_state)


@dp.message(RegistrationState.username_state)
async def enter_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('language')
    text = Tools.is_correct_name_message(message.text, phrases, lang)
    keyboard = None
    next_state = False

    if text == "correct message":
        text = phrases['phrases']['selectMonth'][lang]
        keyboard = months_keyboard(phrases, lang)
        next_state = True
    await message.answer(text=text, reply_markup=keyboard)
    if next_state:
        await state.update_data(name=message.text)
        await state.set_state(RegistrationState.month_state)


@dp.message(RegistrationState.month_state)
async def input_month_of_birth(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('language')
    month_number = Tools.get_month_number(message.text, lang)

    if month_number:
        text = phrases['phrases']['selectDay'][lang]
        await message.answer(text=text, reply_markup=days_keyboard(month_number))
        await state.update_data(month = month_number)
        await state.set_state(RegistrationState.day_state)
    else:
        await message.delete()


@dp.message(RegistrationState.day_state)
async def input_day_of_birth(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('language')
    month_number = state_data.get('month')
    day = Tools.correct_day(message.text, month_number)

    if day:
        await state.update_data(day=day)
        data = Tools.unpack_state_data(await state.get_data())
        datasource.add_new_user(tg_id=message.from_user.id, data=data)
        text = phrases['phrases']['registrationDone'][lang]
        menu = phrases['main'][lang]
        await message.answer(text=text)
        await message.answer(text=menu, reply_markup=main_keyboard())
        await state.clear()
    else:
        await message.delete()
