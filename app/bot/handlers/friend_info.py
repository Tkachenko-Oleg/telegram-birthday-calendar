from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F


from app.bot.main import dp, datasource, phrases
from app.bot.services.tools import Tools
from app.bot.states.friends import FriendsState
from app.bot.keyboards import remove_keyboard, info_keyboard


@dp.message(FriendsState.friends_is_active, F.text.startswith('ℹ️'))
async def show_friend_info(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    text = phrases['phrases']['inputNicknameInfoFriend'][lang]
    await message.answer(text=text)
    await state.set_state(FriendsState.friend_info)


@dp.message(FriendsState.friend_info)
async def show_friend_info(message: Message, state: FSMContext):
    # if datasource.check_relationship(usr_id, contact_id):
    #     await message
    await message.answer("Функция в разработке")
