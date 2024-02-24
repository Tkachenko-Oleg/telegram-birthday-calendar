from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from states import FormChangeUserProfile
from main import dp, tools, datasource, phrases, panels

@dp.message(Command('change_profile'))
async def change_user_profile_command_handler(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    if usr_id:
        lang = datasource.get_lang(usr_id)
        text = phrases['phrases']['changeSetting'][lang]
        await state.set_state(FormChangeUserProfile.choice)
        await message.answer(text=text, reply_markup=panels.changes_panel(phrases, lang))
    else:
        await message.answer("You are not registered")


@dp.message(FormChangeUserProfile.choice)
async def identify_change(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)

    if message.text == phrases['phrases']['changeLanguage'][lang]:
        text = phrases['phrases']['selectLanguage'][lang]
        await message.answer(text=text, reply_markup=panels.language_panel())
        await state.set_state(FormChangeUserProfile.language)

    elif message.text == phrases['phrases']['changeName'][lang]:
        text = phrases['phrases']['enterName'][lang]
        await message.answer(text=text, reply_markup=panels.remove_panel())
        await state.set_state(FormChangeUserProfile.name)

    elif message.text == phrases['phrases']['changeBirthday'][lang]:
        text = phrases['phrases']['selectMonth'][lang]
        await message.answer(text=text, reply_markup=panels.month_panel(phrases, lang))
        await state.set_state(FormChangeUserProfile.birth_month)

    else:
        text = phrases['phrases']['changeSetting'][lang]
        await message.answer(text=text, reply_markup=panels.changes_panel(phrases, lang))



@dp.message(FormChangeUserProfile.language)
async def change_language(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)

    match message.text:
        case 'Русский 🇷🇺':
            datasource.change_language(usr_id, 'Ru')
            text = phrases['phrases']['updateProfile']['Ru']
            await message.answer(text=text, reply_markup=panels.commands_panel())
            await state.clear()
        case 'English 🇬🇧':
            datasource.change_language(usr_id, 'En')
            text = phrases['phrases']['updateProfile']['En']
            await message.answer(text=text, reply_markup=panels.commands_panel())
            await state.clear()
        case _:
            text = phrases['phrases']['selectLanguage'][lang]
            await message.answer(text=text, reply_markup=panels.language_panel())


@dp.message(FormChangeUserProfile.name)
async def change_name(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)
    mes_text = message.text

    if mes_text:
        if len(mes_text) <= 50:
            datasource.change_name(usr_id, mes_text)
            text = phrases['phrases']['updateProfile']['Ru']
            await message.answer(text=text, reply_markup=panels.commands_panel())
            await state.clear()
        else:
            text = phrases['phrases']['longMessage'][lang]
            await message.answer(text=text)
    else:
        text = phrases['phrases']['textMessage'][lang]
        await message.answer(text=text)


@dp.message(FormChangeUserProfile.birth_month)
async def change_month(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)
    month_number = tools.get_month_number(message.text, lang)

    if month_number:
        text = phrases['phrases']['selectDay'][lang]
        await state.update_data(birth_month=month_number)
        await message.answer(text=text, reply_markup=panels.day_panel(month_number))
        await state.set_state(FormChangeUserProfile.birthday)
    else:
        text = phrases['phrases']['selectMonth'][lang]
        await message.answer(text=text, reply_markup=panels.month_panel(phrases, lang))


@dp.message(FormChangeUserProfile.birthday)
async def change_day(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)
    month_number = dict(await state.get_data()).get('birth_month')
    user_day = tools.correct_day(message.text, month_number)

    if user_day:
        text = phrases['phrases']['updateProfile'][lang]
        datasource.change_birthday(usr_id, month_number, user_day)
        await message.answer(text=text, reply_markup=panels.commands_panel())
        await state.clear()
    else:
        if message.text == 'ᅠ':
            await message.delete()
        text = phrases['phrases']['selectDay'][lang]
        await message.answer(text=text, reply_markup=panels.day_panel(month_number))
