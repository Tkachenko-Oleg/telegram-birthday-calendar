from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from states import FormChangeUserProfile
from main import dp, tools, datasource

@dp.message(Command('change_my_profile'))
async def change_user_profile_command_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(message.from_user.id)
    if is_exist_user_profile:
        button_language = InlineKeyboardButton(text="language", callback_data="change_user_language")
        button_username = InlineKeyboardButton(text="username", callback_data="change_user_username")
        button_birth_date = InlineKeyboardButton(text="birth date", callback_data="change_user_birth_date")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_language, button_username, button_birth_date]])
        await message.answer("What options do you want to change?", reply_markup=keyboard)
    else:
        await message.answer("You are not registered")

@dp.callback_query(F.data == "change_user_language")
async def change_user_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FormChangeUserProfile.language)
    await callback.message.answer("Input new language")
    await callback.message.delete()

@dp.message(FormChangeUserProfile.language)
async def input_new_language(message: Message):
    user_id = message.from_user.id
    new_language = message.text
    datasource.change_user_profile(user_id, 'language', new_language)
    await message.answer(f"Your new profile:\n\n{datasource.show_user_profile(user_id)}")

@dp.callback_query(F.data == "change_user_username")
async def change_user_username(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FormChangeUserProfile.username)
    await callback.message.answer("Input new username")
    await callback.message.delete()

@dp.message(FormChangeUserProfile.username)
async def input_new_username(message: Message):
    user_id = message.from_user.id
    new_username = message.text
    datasource.change_user_profile(user_id, 'username', new_username)
    await message.answer(f"Your new profile:\n\n{datasource.show_user_profile(user_id)}")

@dp.callback_query(F.data == "change_user_birth_date")
async def change_user_birth_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FormChangeUserProfile.year_of_birth)
    await callback.message.answer("Input new year of birth")
    await callback.message.delete()

@dp.message(FormChangeUserProfile.year_of_birth)
async def input_new_year(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(year_of_birth=message.text)
        if tools.check_correct_data(await state.get_data()):
            await state.set_state(FormChangeUserProfile.month_of_birth)
            await message.answer("Input month of birth: ")
        else:
            await message.answer("The year is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birth year")

@dp.message(FormChangeUserProfile.month_of_birth)
async def input_new_month(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(month_of_birth=message.text)
        if tools.check_correct_data(await state.get_data()):
            await state.set_state(FormChangeUserProfile.day_of_birth)
            await message.answer("Input day of birth: ")
        else:
            await message.answer("The month is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birth month")

@dp.message(FormChangeUserProfile.day_of_birth)
async def input_new_day(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(day_of_birth=message.text)
        if tools.check_correct_data(await state.get_data()):
            user_id = message.from_user.id
            datasource.change_user_profile(user_id, 'birth_date', await state.get_data())
            await state.clear()
            await message.answer(f"Your new profile:\n\n{datasource.show_user_profile(user_id)}")
        else:
            await message.answer("The day is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birthday")
