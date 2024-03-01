from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from main import dp, tools, datasource, phrases, panels
from states import FormChangeUserProfile

@dp.message(Command('change_profile'))
async def change_user_profile_command_handler(message: Message, state: FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['changeSetting'][lang]
        await state.set_state(FormChangeUserProfile.choice)
        await message.answer(text=text, reply_markup=panels.changes_panel(phrases, lang))
    else:
        await message.answer("You are not registered")


@dp.message(FormChangeUserProfile.choice)
async def identify_change(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
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
    lang = datasource.get_lang(tg_id=message.from_user.id)
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
        await message.answer(text=text, reply_markup=panels.commands_panel())
        await state.clear()
    else:
        text = phrases['phrases']['selectLanguage'][lang]
        await message.answer(text=text, reply_markup=panels.language_panel())


@dp.message(FormChangeUserProfile.name)
async def change_name(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    message_type = tools.is_correct_name_message(message.text)
    is_name_changed = False
    panel = None

    if message_type == 'non-textual':
        text = phrases['phrases']['textMessage'][lang]
    elif message_type == 'long message':
        text = phrases['phrases']['longMessage'][lang]
    else:
        text = phrases['phrases']['updateProfile'][lang]
        panel = panels.commands_panel()
        is_name_changed = True

    await message.answer(text=text, reply_markup=panel)
    if is_name_changed:
        datasource.change_name(tg_id=message.from_user.id, name=message.text)
        await state.clear()


@dp.message(FormChangeUserProfile.birth_month)
async def change_month(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
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
    lang = datasource.get_lang(tg_id=message.from_user.id)
    month_number = dict(await state.get_data()).get('birth_month')
    user_day = tools.correct_day(message.text, month_number)

    if user_day:
        text = phrases['phrases']['updateProfile'][lang]
        datasource.change_birthday(tg_id=message.from_user.id, birth_month=month_number, birthday=user_day)
        await message.answer(text=text, reply_markup=panels.commands_panel())
        await state.clear()
    else:
        if message.text == 'ᅠ':
            await message.delete()
        text = phrases['phrases']['selectDay'][lang]
        await message.answer(text=text, reply_markup=panels.day_panel(month_number))
