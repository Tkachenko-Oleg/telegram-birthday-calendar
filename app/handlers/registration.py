from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F

from states import FormRegistration
from main import dp, tools, datasource
from services import Panels


@dp.message(Command('start'))
async def start_registration_command_handler(message: Message, state: FSMContext):
    if not datasource.check_exist_user(str(message.from_user.id)):
        await state.update_data(tg_id=message.from_user.id)
        await message.answer(f"{message.from_user.full_name} 👋", reply_markup=Panels.language_panel())
    else:
        await message.answer("You are already registered")


@dp.message((F.text == "Русский 🇷🇺") | (F.text == "English 🇬🇧"))
async def registration_input_language_ru(message: Message, state: FSMContext):
    if message.text == "Русский 🇷🇺":
        await state.update_data(language='Ru')
    elif message.text == "English 🇬🇧":
        await state.update_data(language='En')
    else:
        pass

    await message.answer("Please, click the button to share your phone number", reply_markup=Panels.contact_panel())
    await state.set_state(FormRegistration.phone_number)


@dp.message(FormRegistration.phone_number)
async def registration_input_phone_number(message: Message, state: FSMContext):
    try:
        await state.update_data(phone_number=message.contact.phone_number)
        await message.answer("Input unique nickname: ", reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormRegistration.nickname)
    except AttributeError:
        await message.answer("Please, click the button")


@dp.message(FormRegistration.nickname)
async def registration_input_nickname(message: Message, state: FSMContext):
    if message.text:
        if not datasource.check_exist_nickname(message.text):
            await state.update_data(nickname=message.text)
            await message.answer("Input name: ")
            await state.set_state(FormRegistration.username)
        else:
            await message.answer("This nickname already exists")
    else:
        await message.answer("Please enter a text message with your nickname")


@dp.message(FormRegistration.username)
async def registration_input_name(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(username=message.text)
        await message.answer("Input month of birth: ", reply_markup=Panels.month_panel().as_markup(resize_keyboard=True))
        await state.set_state(FormRegistration.month_of_birth)
    else:
        await message.answer("Please enter a text message with your name")


@dp.message(FormRegistration.month_of_birth)
async def registration_input_month_of_birth(message: Message, state: FSMContext):
    user_month = tools.convert_string_to_integer_month(message.text)
    if user_month:
        await state.update_data(month_of_birth=user_month)
        await message.answer("Input day of birth: ", reply_markup=Panels.day_panel(user_month).as_markup(resize_keyboard=True))
        await state.set_state(FormRegistration.day_of_birth)
    else:
        await message.answer("Please, click the button")


@dp.message(FormRegistration.day_of_birth)
async def registration_input_day_of_birth(message: Message, state: FSMContext):
    if message.text != 'ᅠ' and message.text.isdigit():
        user_day = tools.correct_day(message.text)

        if user_day:
            await state.update_data(day_of_birth=message.text)
            datasource.add_user_to_main_database(await state.get_data())
            await message.answer("You have been registered", reply_markup=Panels.commands_panel())
            await state.clear()
        else:
            await message.answer("Please, click the button")
    else:
        await message.delete()
        await message.answer("Please, click the button with number")
