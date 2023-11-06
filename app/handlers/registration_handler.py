from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from states import FormRegistration
from main import tools

from main import dp


@dp.message(Command('start'))
async def start_registration_command_handler(message: Message, state: FSMContext):
    await message.answer(f"Hello, {message.from_user.full_name}!\nBot is running!")
    await state.set_state(FormRegistration.language)
    await message.answer("Input language: ")

@dp.message(FormRegistration.language)
async def registration_input_language(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(language=message.text)
        await state.set_state(FormRegistration.phone_number)
        button = [[KeyboardButton(text='registration', request_contact=True)]]
        panel = ReplyKeyboardMarkup(keyboard=button)
        await message.answer("Please, click the button to share your phone number", reply_markup=panel)
    else:
        await message.answer("Please enter a text message indicating your language")

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
    if message.text:
        await state.update_data(nickname=message.text)
        await state.set_state(FormRegistration.name)
        await message.answer("Input name: ")
    else:
        await message.answer("Please enter a text message with your nickname")

@dp.message(FormRegistration.name)
async def registration_input_name(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(name=message.text)
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
            state_dict = dict(await state.get_data())
            print(state_dict)
            await message.answer(f"language: {state_dict['language']}\n"
                                 f"phone number: {state_dict['phone_number']}\n"
                                 f"nickname: {state_dict['nickname']}\n"
                                 f"name: {state_dict['name']}\n"
                                 f"year of birth: {state_dict['year_of_birth']}\n"
                                 f"month of birth: {state_dict['month_of_birth']}\n"
                                 f"day of birth: {state_dict['day_of_birth']}")

            await state.clear()
        else:
            await message.answer("The day is incorrect!")
    else:
        await message.answer("Please enter a number-only text message with your birthday")
