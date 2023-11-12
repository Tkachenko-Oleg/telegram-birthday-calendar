from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F

from main import dp, datasource


@dp.message(Command('delete_my_profile'))
async def delete_user_profile_command_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(message.from_user.id)
    if is_exist_user_profile:
        button_yes = InlineKeyboardButton(text="yes", callback_data="delete_user_profile")
        button_no = InlineKeyboardButton(text="no", callback_data="not_delete_user_profile")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_yes, button_no]])
        await message.answer("Are you sure?", reply_markup=keyboard)
    else:
        await message.answer("You are not registered")

@dp.callback_query(F.data == "delete_user_profile")
async def delete_user_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    datasource.delete_profile(user_id)
    await callback.message.answer("Your profile has been deleted")
    await callback.message.delete()

@dp.callback_query(F.data == "not_delete_user_profile")
async def info_message(callback: CallbackQuery):
    await callback.message.answer("Your profile has not been deleted")
    await callback.message.delete()
