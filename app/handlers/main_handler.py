from aiogram.types import Message
from aiogram.filters import Command

from main import dp


@dp.message(Command('start'))
async def start_command_handler(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!\nBot is running")


# @dp.message()
# async def echo(message: Message):
#     # print(message.contact.user_id,
#     #       message.contact.first_name,
#     #       message.contact.phone_number)
#
#     # print(message.contact)
#     # print(message.from_user.id)
#
