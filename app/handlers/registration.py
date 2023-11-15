from aiogram import F
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import FormRegistration
from main import dp, tools, datasource


@dp.message(Command('start'))
async def start_registration_command_handler(message: Message, state: FSMContext):
    user = message.from_user
    if not datasource.check_exist_user(str(user.id)):
        await message.answer(f"Hello, {user.full_name}!\nBot is running!")
        await state.update_data(tg_id=user.id)
        button_ru = InlineKeyboardButton(text="Ru", callback_data="reg_button_ru")
        button_en = InlineKeyboardButton(text="En", callback_data="reg_button_en")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_ru, button_en]])
        await message.answer("Choose a language", reply_markup=keyboard)
    else:
        await message.answer("You are already registered")

@dp.callback_query(F.data == 'reg_button_ru')
async def registration_input_language_ru(callback: CallbackQuery, state: FSMContext):
    reg_button = [[KeyboardButton(text='registration', request_contact=True)]]
    panel = ReplyKeyboardMarkup(keyboard=reg_button)
    await state.update_data(language='Ru')
    await state.set_state(FormRegistration.phone_number)
    await callback.message.answer("Please, click the button to share your phone number", reply_markup=panel)

@dp.callback_query(F.data == 'reg_button_en')
async def registration_input_language_en(callback: CallbackQuery, state: FSMContext):
    reg_button = [[KeyboardButton(text='registration', request_contact=True)]]
    panel = ReplyKeyboardMarkup(keyboard=reg_button)
    await state.update_data(language='En')
    await state.set_state(FormRegistration.phone_number)
    await callback.message.answer("Please, click the button to share your phone number", reply_markup=panel)

@dp.message(FormRegistration.phone_number)
async def registration_input_phone_number(message: Message, state: FSMContext):
    try:
        await state.update_data(phone_number=message.contact.phone_number)
        await state.set_state(FormRegistration.nickname)
        await message.answer("Input unique nickname: ")
    except AttributeError:
        await message.answer("Please, click the button")

@dp.message(FormRegistration.nickname)
async def registration_input_nickname(message: Message, state: FSMContext):
    nickname = message.text
    if nickname:
        if not datasource.check_exist_nickname(nickname):
            await state.update_data(nickname=nickname)
            await state.set_state(FormRegistration.username)
            await message.answer("Input name: ")
        else:
            await message.answer("This nickname already exists")
    else:
        await message.answer("Please enter a text message with your nickname")

@dp.message(FormRegistration.username)
async def registration_input_name(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(username=message.text)
        await state.set_state(FormRegistration.year_of_birth)
        await message.answer("Input year of birth: ")
    else:
        await message.answer("Please enter a text message with your name")

@dp.message(FormRegistration.year_of_birth)
async def registration_input_year_of_birth(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(year_of_birth=message.text)
        if tools.check_correct_data(await state.get_data()):
            await state.set_state(FormRegistration.month_of_birth)
            await message.answer("Input month of birth: ")
        else:
            await message.answer("The year is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birth year")

@dp.message(FormRegistration.month_of_birth)
async def registration_input_month_of_birth(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(month_of_birth=message.text)
        if tools.check_correct_data(await state.get_data()):
            await state.set_state(FormRegistration.day_of_birth)
            await message.answer("Input day of birth: ")
        else:
            await message.answer("The month is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birth month")

@dp.message(FormRegistration.day_of_birth)
async def registration_input_day_of_birth(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(day_of_birth=message.text)
        if tools.check_correct_data(await state.get_data()):
            datasource.add_user_to_main_database(await state.get_data())
            await state.clear()
            await message.answer("You have been registered")
        else:
            await message.answer("The day is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birthday")
