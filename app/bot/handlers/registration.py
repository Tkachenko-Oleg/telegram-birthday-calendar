from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from main import dp, tools, datasource, phrases, panels
from states import FormRegistration


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not datasource.is_user_exist(tg_id=message.from_user.id):
        await message.answer(f"{message.from_user.full_name} 👋")
        await message.answer("🇬🇧: Choose language\n🇷🇺: Выберете язык", reply_markup=panels.language_panel())
        await state.set_state(FormRegistration.language)
    else:
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['alreadyReg'][lang]
        await message.answer(text=text, reply_markup=panels.commands_panel())


@dp.message(FormRegistration.language)
async def input_language(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    is_lang_selected = True
    curr_lang = 'En'

    if message.text == "Русский 🇷🇺":
        curr_lang = 'Ru'
    elif message.text == "English 🇬🇧":
        curr_lang = 'En'
    else:
        is_lang_selected = False

    if is_lang_selected:
        text = phrases['phrases']['regButton'][curr_lang]
        await state.update_data(language=curr_lang)
        await message.answer(text=text, reply_markup=panels.contact_panel(phrases, curr_lang))
        await state.set_state(FormRegistration.phone_number)
    else:
        await message.delete()


@dp.message(FormRegistration.phone_number)
async def input_phone_number(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    if message.contact:
        text = phrases['phrases']['enterNickname'][lang]
        await state.update_data(phone_number=message.contact.phone_number)
        await message.answer(text=text, reply_markup=panels.remove_panel())
        await state.set_state(FormRegistration.nickname)
    else:
        await message.delete()


@dp.message(FormRegistration.nickname)
async def input_nickname(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    message_type = tools.is_correct_name_message(message.text)
    next_state = False

    if message_type == 'non-textual':
        text = phrases['phrases']['textMessage'][lang]
    elif message_type == 'long message':
        text = phrases['phrases']['longMessage'][lang]
    else:
        if not datasource.is_nickname_exist(nickname=message.text):
            text = phrases['phrases']['enterName'][lang]
            next_state = True
        else:
            text = phrases['phrases']['nicknameExist'][lang]

    await message.answer(text=text)
    if next_state:
        await state.update_data(nickname=message.text)
        await state.set_state(FormRegistration.name)


@dp.message(FormRegistration.name)
async def input_name(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    message_type = tools.is_correct_name_message(message.text)
    panel = None
    next_state = False

    if message_type == 'non-textual':
        text = phrases['phrases']['textMessage'][lang]
    elif message_type == 'long message':
        text = phrases['phrases']['longMessage'][lang]
    else:
        text = phrases['phrases']['selectMonth'][lang]
        panel = panels.month_panel(phrases, lang)
        next_state = True

    await message.answer(text=text, reply_markup=panel)
    if next_state:
        await state.update_data(name=message.text)
        await state.set_state(FormRegistration.birth_month)


@dp.message(FormRegistration.birth_month)
async def input_month_of_birth(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    month_number = tools.get_month_number(message.text, lang)

    if month_number:
        text = phrases['phrases']['selectDay'][lang]
        await state.update_data(birth_month = month_number)
        await message.answer(text=text, reply_markup=panels.day_panel(month_number))
        await state.set_state(FormRegistration.birthday)
    else:
        text = phrases['phrases']['selectMonth'][lang]
        await message.answer(text=text, reply_markup=panels.month_panel(phrases, lang))


@dp.message(FormRegistration.birthday)
async def input_day_of_birth(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    month_number = dict(await state.get_data()).get('birth_month')
    user_day = tools.correct_day(message.text, month_number)

    if user_day:
        await state.update_data(birthday=user_day)
        text = phrases['phrases']['registrationDone'][lang]
        data = tools.unpack_state_data(await state.get_data())
        datasource.add_new_user(tg_id=message.from_user.id, data=data)
        await message.answer(text=text, reply_markup=panels.commands_panel())
        await state.clear()
    else:
        if message.text == 'ᅠ':
            await message.delete()
        text = phrases['phrases']['selectDay'][lang]
        await message.answer(text=text, reply_markup=panels.day_panel(month_number))
