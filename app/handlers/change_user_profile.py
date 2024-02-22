from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from services import Panels
from states import FormChangeUserProfile
from main import dp, tools, datasource

@dp.message(Command('change_my_profile'))
async def change_user_profile_command_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(str(message.from_user.id))
    if is_exist_user_profile:
        await message.answer("What options do you want to change?", reply_markup=Panels.changes_panel())
    else:
        await message.answer("You are not registered")


@dp.message((F.text == 'change language') | (F.text == 'change name') | (F.text == 'change birthday'))
async def identify_change(message: Message, state: FSMContext):
    if message.text == 'change language':
        await message.answer("Choose a language", reply_markup=Panels.change_language_panel())

    elif message.text == 'change name':
        await message.answer("Input new username")
        await state.set_state(FormChangeUserProfile.name)

    elif message.text == 'change birthday':
        await message.answer("Input month of birth: ", reply_markup=Panels.month_panel().as_markup(resize_keyboard=True))
        await state.set_state(FormChangeUserProfile.month_of_birth)

    else:
        pass


@dp.message((F.text == "Ру 🇷🇺") | (F.text == "En 🇬🇧"))
async def change_language(message: Message):
    if message.text == "Ру 🇷🇺":
        datasource.change_user_profile(str(message.from_user.id), 'language', "Ru")
    elif message.text == "En 🇬🇧":
        datasource.change_user_profile(str(message.from_user.id), 'language', "En")
    else:
        pass

    await message.answer(f"Your new profile:\n\n{datasource.show_user_profile(str(message.from_user.id))}",
                         reply_markup=Panels.commands_panel())


@dp.message(FormChangeUserProfile.name)
async def change_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    datasource.change_user_profile(str(message.from_user.id), 'user_name', await state.get_data())

    await message.answer(f"Your new profile:\n\n{datasource.show_user_profile(str(message.from_user.id))}",
                         reply_markup=Panels.commands_panel())
    await state.clear()


@dp.message(FormChangeUserProfile.month_of_birth)
async def change_month(message: Message, state: FSMContext):
    user_month = tools.convert_string_to_integer_month(message.text)
    if user_month:
        await state.update_data(month_of_birth=user_month)
        await message.answer("Input day of birth: ", reply_markup=Panels.day_panel(user_month).as_markup(resize_keyboard=True))
        await state.set_state(FormChangeUserProfile.day_of_birth)
    else:
        await message.answer("Please, click the button")


@dp.message(FormChangeUserProfile.day_of_birth)
async def change_day(message: Message, state: FSMContext):
    if message.text != 'ᅠ' and message.text.isdigit():
        user_day = tools.correct_day(message.text)

        if user_day:
            await state.update_data(day_of_birth=message.text)
            datasource.change_user_profile(str(message.from_user.id), 'birthday', await state.get_data())
            await message.answer(f"Your new profile:\n\n{datasource.show_user_profile(str(message.from_user.id))}",
                                 reply_markup=Panels.commands_panel())
            await state.clear()
        else:
            await message.answer("Please, click the button")
    else:
        await message.delete()
        await message.answer("Please, click the button with number")
