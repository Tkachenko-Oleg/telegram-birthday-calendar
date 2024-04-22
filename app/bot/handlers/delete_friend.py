from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.main import dp, datasource, phrases
from app.bot.states.friends import FriendsState
from app.bot.keyboards import main_keyboard, delete_friend_keyboard, remove_keyboard


@dp.message(FriendsState.friends_is_active, F.text.startswith('✖️'))
async def delete_friend(message: Message, state: FSMContext):
    lang = datasource.get_lang(message.from_user.id)
    text = phrases['phrases']['inputNicknameDelFriend'][lang]
    await message.answer(text=text, reply_markup=remove_keyboard())
    await state.set_state(FriendsState.delete_nickname)


@dp.message(FriendsState.delete_nickname)
async def delete_friend(message: Message, state: FSMContext):
    lang = datasource.get_lang(message.from_user.id)
    if datasource.is_nickname_exist(nickname=message.text):
        text = phrases['phrases']['confirmation'][lang]
        await message.answer(text=text, reply_markup=delete_friend_keyboard(phrases, lang))
        await state.update_data(delete_nickname=message.text)
        await state.set_state(FriendsState.delete_state)
    else:
        text = phrases['phrases']['userNotFound'][lang]
        await message.answer(text=text, reply_markup=main_keyboard())
        await state.clear()


@dp.message(FriendsState.delete_state, F.text.startswith('❌'))
async def delete_friend(message: Message, state: FSMContext):
    lang = datasource.get_lang(message.from_user.id)
    state_data = await state.get_data()
    nickname = state_data.get('delete_nickname')
    datasource.delete_friend(tg_id=message.from_user.id, nickname_friend=nickname)
    text = phrases['phrases']['friendIsDeleted'][lang]
    await message.answer(text=text, reply_markup=main_keyboard())


@dp.message(FriendsState.delete_state, ~F.text.startswith('❌'))
async def delete_friend(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    await message.answer(text=phrases['main'][lang], reply_markup=main_keyboard())
    await state.clear()
