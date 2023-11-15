from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from states import FormSearchUser
from main import dp, datasource

@dp.message(Command('search_user'))
async def search_user(message: Message):
    is_exist_user_profile = datasource.check_exist_user(str(message.from_user.id))
    if is_exist_user_profile:
        button_nickname = InlineKeyboardButton(text="by nickname", callback_data="search_user_by_nickname")
        button_phone_number = InlineKeyboardButton(text="by phone number", callback_data="search_user_by_phone_number")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_nickname, button_phone_number]])
        await message.answer("How do you want to find the user?", reply_markup=keyboard)
    else:
        await message.answer("You are not registered")

@dp.callback_query(F.data == "search_user_by_nickname")
async def start_search_user_by_nickname(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FormSearchUser.nickname)
    await callback.message.answer("Enter the nickname of the user you want to find")
    await callback.message.delete()

@dp.message(FormSearchUser.nickname)
async def search_user_by_nickname(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    nickname = dict(await state.get_data()).get('nickname')
    user_info, unique_id = datasource.search_user_by_nickname(nickname)
    await state.set_state(FormSearchUser.user_id_to_add)
    if user_info:
        await state.update_data(user_id_to_add=unique_id)
        user_id_to_add = dict(await state.get_data()).get('user_id_to_add')
        if datasource.check_the_relationship_database(unique_id, user_id_to_add):
            button_add = InlineKeyboardButton(text="add user to birthday list", callback_data="add_user_to_list")
            button_not_add = InlineKeyboardButton(text="do not add user to birthday list", callback_data="do_not_add_user")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_add, button_not_add]])
            await message.answer(f"{user_info}\n\nHow do you want to find the user?", reply_markup=keyboard)
        else:
            await message.answer("The user has already been added to your birthday list")
    else:
        await message.answer("User not found")

@dp.callback_query(F.data == "search_user_by_phone_number")
async def start_search_user_by_nickname(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FormSearchUser.phone_number)
    await callback.message.answer("Enter the phone number of the user you want to find")
    await callback.message.delete()

@dp.message(FormSearchUser.phone_number)
async def search_user_by_nickname(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    phone_number = dict(await state.get_data()).get('phone_number')
    user_info, unique_id = datasource.search_user_by_phone_number(phone_number)
    await state.set_state(FormSearchUser.user_id_to_add)
    if user_info:
        await state.update_data(user_id_to_add=unique_id)
        user_id_to_add = dict(await state.get_data()).get('user_id_to_add')
        if datasource.check_the_relationship_database(unique_id, user_id_to_add):
            button_add = InlineKeyboardButton(text="add user to birthday list", callback_data="add_user_to_list")
            button_not_add = InlineKeyboardButton(text="do not add user to birthday list", callback_data="do_not_add_user")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_add, button_not_add]])
            await message.answer(f"{user_info}\n\nHow do you want to find the user?", reply_markup=keyboard)
        else:
            await message.answer("The user has already been added to your birthday list")
    else:
        await message.answer("User not found")

@dp.callback_query(F.data == "add_user_to_list")
async def add_user_to_birthday_list(callback: CallbackQuery, state: FSMContext):
    user_id_to_add = dict(await state.get_data()).get('user_id_to_add')
    await state.clear()
    await callback.message.delete()
    if datasource.add_user_birthday_to_relation_database(str(callback.from_user.id), user_id_to_add):
        await callback.message.answer("The user has been added to your birthday list")
    else:
        await callback.message.answer("The user has not been added to your birthday list")

@dp.callback_query(F.data == "do_not_add_user")
async def do_not_add_user_to_birthday_list(callback: CallbackQuery):
    await callback.message.answer("User not added")
    await callback.message.delete()
