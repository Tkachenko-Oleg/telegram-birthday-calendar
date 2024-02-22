from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F

from services import Panels
from main import dp, datasource


@dp.message(Command('delete_my_profile'))
async def delete_user_profile_command_handler(message: Message):
    is_exist_user_profile = datasource.check_exist_user(str(message.from_user.id))
    if is_exist_user_profile:
        await message.answer("Are you sure?", reply_markup=Panels.delete_profile())
    else:
        await message.answer("You are not registered")


@dp.message((F.text == 'delete profile ✅') | (F.text == 'do not delete profile ❌'))
async def delete_profile(message: Message):
    if message.text == 'delete profile ✅':
        user_id = datasource.get_id_user(str(message.from_user.id))
        datasource.delete_profile(user_id)
        await message.answer("Your profile has been deleted", reply_markup=ReplyKeyboardRemove())
    elif message.text == 'do not delete profile ❌':
        await message.answer("Your profile has not been deleted", reply_markup=ReplyKeyboardRemove())
