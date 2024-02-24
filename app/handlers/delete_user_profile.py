from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from main import dp, datasource, phrases, panels
from states import FormDeleteProfile



@dp.message(Command('delete_profile'))
async def delete_user_profile_command_handler(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    if usr_id:
        lang = datasource.get_lang(usr_id)
        text = phrases['phrases']['confirmation'][lang]
        await message.answer(text=text, reply_markup=panels.delete_profile(phrases, lang))
        await state.set_state(FormDeleteProfile.delete_state)
    else:
        await message.answer("You are not registered")


@dp.message(FormDeleteProfile.delete_state)
async def delete_profile(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)
    if message.text == phrases['phrases']['questDelProfile'][lang]:
        text = phrases['phrases']['messageDelProfile'][lang]
        datasource.delete_profile(usr_id)
        await message.answer(text=text, reply_markup=panels.remove_panel())
        await state.clear()
    else:
        text = phrases['phrases']['messageNotDelProfile'][lang]
        await message.answer(text=text, reply_markup=panels.commands_panel())
        await state.clear()
