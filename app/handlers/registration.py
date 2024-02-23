from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from main import dp, tools, datasource, panels, phrases
from states import FormRegistration


@dp.message(Command('start'))
async def start_registration_command_handler(message: Message, state: FSMContext):
    usr_id = str(message.from_user.id)
    if not datasource.get_id(usr_id):
        await message.answer(f"{message.from_user.full_name} 👋", reply_markup=panels.language_panel())
        await state.set_state(FormRegistration.language)
    else:
        lang = datasource.get_lang(datasource.get_id(usr_id))
        text = phrases['phrases']['alreadyReg'][lang]
        await message.answer(text=text)


@dp.message(FormRegistration.language)
async def registration_input_language_ru(message: Message, state: FSMContext):
    await state.update_data(tg_id=str(message.from_user.id))
    is_lang_selected = False

    match message.text:
        case "Русский 🇷🇺":
            await state.update_data(language='Ru')
            text = phrases['phrases']['regButton']['Ru']
            is_lang_selected = True
        case "English 🇬🇧":
            await state.update_data(language='En')
            text = phrases['phrases']['regButton']['En']
            is_lang_selected = True
        case _:
            text = "🇬🇧: Choose language\n🇷🇺: Выберете язык"

    if is_lang_selected:
        lang = dict(await state.get_data()).get('language')
        await message.answer(text=text, reply_markup=panels.contact_panel(phrases, lang))
        await state.set_state(FormRegistration.phone_number)
    else:
        await message.answer(text=text, reply_markup=panels.language_panel())


@dp.message(FormRegistration.phone_number)
async def registration_input_phone_number(message: Message, state: FSMContext):
    contact = message.contact
    lang = dict(await state.get_data()).get('language')
    if contact:
        text = phrases['phrases']['enterNickname'][lang]
        await state.update_data(phone_number=contact.phone_number)
        await message.answer(text=text, reply_markup=panels.remove_panel())
        await state.set_state(FormRegistration.nickname)
    else:
        text = phrases['phrases']['regButton'][lang]
        await message.answer(text=text, reply_markup=panels.contact_panel(phrases, lang))


@dp.message(FormRegistration.nickname)
async def registration_input_nickname(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    mes_text = message.text
    if mes_text:
        if len(mes_text) <= 50:
            if not datasource.is_nickname_exist(mes_text):
                text = phrases['phrases']['enterName'][lang]
                await state.update_data(nickname=mes_text)
                await message.answer(text=text)
                await state.set_state(FormRegistration.name)
            else:
                text = phrases['phrases']['nicknameExist'][lang]
                await message.answer(text=text)
        else:
            text = phrases['phrases']['longMessage'][lang]
            await message.answer(text=text)
    else:
        text = phrases['phrases']['textMessage'][lang]
        await message.answer(text=text)


@dp.message(FormRegistration.name)
async def registration_input_name(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    mes_text = message.text
    if mes_text:
        if len(mes_text) <= 50:
            text = phrases['phrases']['selectMonth'][lang]
            await state.update_data(name=mes_text)
            await message.answer(text=text, reply_markup=panels.month_panel(phrases, lang))
            await state.set_state(FormRegistration.birth_month)
        else:
            text = phrases['phrases']['longMessage'][lang]
            await message.answer(text=text)
    else:
        text = phrases['phrases']['textMessage'][lang]
        await message.answer(text=text)


@dp.message(FormRegistration.birth_month)
async def registration_input_month_of_birth(message: Message, state: FSMContext):
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
async def registration_input_day_of_birth(message: Message, state: FSMContext):
    lang = dict(await state.get_data()).get('language')
    month_number = dict(await state.get_data()).get('birth_month')
    user_day = tools.correct_day(message.text, month_number)

    if user_day:
        await state.update_data(birthday=user_day)
        data = tools.unpack_state_data(await state.get_data())
        text = phrases['phrases']['registrationDone'][lang]
        datasource.add_new_user_id(str(message.from_user.id))
        usr_id = datasource.get_id(str(message.from_user.id))
        datasource.add_new_user_info(usr_id, data)
        await message.answer(text=text, reply_markup=panels.commands_panel())
        await state.clear()
    else:
        if message.text == 'ᅠ':
            await message.delete()
        text = phrases['phrases']['selectDay'][lang]
        await message.answer(text=text, reply_markup=panels.day_panel(month_number))
