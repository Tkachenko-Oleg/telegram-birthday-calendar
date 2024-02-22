from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.content_type import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F

from services import Panels
from states import FormSearchUser
from main import dp, datasource


@dp.message(Command('search_user'))
async def method_for_search_contact_handler(message: Message, state :FSMContext):
    user_id = datasource.get_id_user(str(message.from_user.id))
    await state.update_data(user_id=user_id)
    await message.answer("Select a search method", reply_markup=Panels.search_user_methods(message.from_user.id))


@dp.message((F.content_type == ContentType.USER_SHARED) | (F.text == 'search with nickname'))
async def search_contact_handler(message: Message, state: FSMContext):
    if message.content_type == ContentType.USER_SHARED:
        contact_id = datasource.search_contact(tg_id=str(message.user_shared.user_id))
        contact_data = datasource.search_contact_info(tg_id=str(message.user_shared.user_id))
        if contact_id and contact_data:
            await state.update_data(contact_id=contact_id)
            await message.answer(f"{contact_data}", reply_markup=ReplyKeyboardRemove())
            await message.answer(f"Do you want add birthday in your list?", reply_markup=Panels.add_contact())
        else:
            await message.answer("User not found", reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(FormSearchUser.contact_id)
        await message.answer("Enter nickname", reply_markup=ReplyKeyboardRemove())


@dp.message(FormSearchUser.contact_id)
async def search_contact_nickname(message: Message, state: FSMContext):
    contact_id = datasource.search_contact(nickname=message.text)
    contact_data = datasource.search_contact_info(nickname=message.text)
    user_id = dict(await state.get_data())['user_id']

    if contact_id and contact_data:
        await state.clear()
        await state.update_data(user_id = user_id, contact_id=contact_id)
        await message.answer(f"{contact_data}")
        await message.answer(f"Do you want add birthday in your list?", reply_markup=Panels.add_contact())
    else:
        await message.answer("User not found")
        await state.clear()


@dp.message((F.text == "add birthday in my list ✅") | (F.text == "don't add birthday ❌"))
async def add_contact(message: Message, state: FSMContext):
    if message.text == "add birthday in my list ✅":
        ids = dict(await state.get_data())
        user_id = ids['user_id']
        contact_id = ids['contact_id']
        if user_id != contact_id:
            if datasource.check_the_relationship_database(user_id, contact_id):
                datasource.add_user_birthday_to_relation_database(user_id, contact_id)
                await message.answer("User has been added", reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer("User already was added", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("You can not adding yourself to birthday list", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("user not added in birthday list", reply_markup=ReplyKeyboardRemove())
