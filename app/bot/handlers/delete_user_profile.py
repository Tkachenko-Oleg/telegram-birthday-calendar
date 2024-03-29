from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from main import dp, datasource, phrases, panels
from states import FormDeleteProfile



@dp.message(Command('delete_profile'))
async def delete_user_profile_command_handler(message: Message, state: FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['confirmation'][lang]
        await message.answer(text=text, reply_markup=panels.delete_profile(phrases, lang))
        await state.set_state(FormDeleteProfile.delete_state)
    else:
        await message.answer("You are not registered")


@dp.message(FormDeleteProfile.delete_state)
async def delete_profile(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    if message.text == phrases['phrases']['questDelProfile'][lang]:
        text = phrases['phrases']['messageDelProfile'][lang]
        datasource.delete_profile(tg_id=message.from_user.id)
        panel = panels.remove_panel()
    else:
        text = phrases['phrases']['messageNotDelProfile'][lang]
        panel = panels.commands_panel()

    await message.answer(text=text, reply_markup=panel)
    await state.clear()
