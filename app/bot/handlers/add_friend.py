from aiogram.types import Message
from aiogram.enums.content_type import ContentType
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.bot.main import dp, datasource, phrases
from app.bot.services.tools import Tools
from app.bot.states.friends import FriendsState
from app.bot.keyboards import search_keyboard, remove_keyboard, add_contact_keyboard, main_keyboard


@dp.message(FriendsState.friends_is_active, F.text.startswith('➕'))
async def method_for_search_contact_handler(message: Message, state :FSMContext):
    if datasource.is_user_exist(tg_id=message.from_user.id):
        lang = datasource.get_lang(tg_id=message.from_user.id)
        text = phrases['phrases']['searchMethod'][lang]
        await message.answer(text=text, reply_markup=search_keyboard(message.from_user.id, phrases, lang))
        await state.set_state(FriendsState.search_method)
    else:
        await message.answer("You are not registered")


@dp.message(FriendsState.search_method)
async def choose_method(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    if message.content_type and message.content_type == ContentType.USER_SHARED:
        contact_id = datasource.get_id(tg_id=message.user_shared.user_id)
        if contact_id:
            postgres_data = datasource.user_profile(tg_id=message.user_shared.user_id)
            contact_info = Tools.parse_postgres(postgres_data, phrases, lang)
            text = phrases['phrases']['questAddUser'][lang]
            await state.update_data(contact_id=contact_id)
            await message.answer(text=contact_info, reply_markup=remove_keyboard())
            await message.answer(text=text, reply_markup=add_contact_keyboard(phrases, lang))
            await state.set_state(FriendsState.add_state)
        else:
            text = phrases['phrases']['userNotFound'][lang]
            await message.answer(text=text, reply_markup=main_keyboard())
            await state.clear()

    elif message.text == phrases['phrases']['searchNick'][lang]:
        text = phrases['phrases']['enterNickname'][lang]
        await message.answer(text=text, reply_markup=remove_keyboard())
        await state.set_state(FriendsState.nickname_state)

    else:
        text = phrases['main'][lang]
        await message.answer(text=text, reply_markup=main_keyboard())
        await state.clear()


@dp.message(FriendsState.nickname_state)
async def search_nickname_contact(message: Message, state: FSMContext):
    lang = datasource.get_lang(tg_id=message.from_user.id)
    if datasource.is_nickname_exist(nickname=message.text):
        contact_tg_id = datasource.get_tg_id_by_nickname(nickname=message.text)
        postgres_data = datasource.user_profile(tg_id=contact_tg_id)
        contact_info = Tools.parse_postgres(postgres_data, phrases, lang)
        text = phrases['phrases']['questAddUser'][lang]
        await state.update_data(contact_id=datasource.get_id(contact_tg_id))
        await message.answer(text=contact_info, reply_markup=remove_keyboard())
        await message.answer(text=text, reply_markup=add_contact_keyboard(phrases, lang))
        await state.set_state(FriendsState.add_state)
    else:
        text = phrases['phrases']['userNotFound'][lang]
        await message.answer(text=text, reply_markup=main_keyboard())
        await state.clear()


@dp.message(FriendsState.add_state)
async def add_contact(message: Message, state: FSMContext):
    usr_id = datasource.get_id(tg_id=message.from_user.id)
    lang = datasource.get_lang(tg_id=message.from_user.id)
    contact_id = dict(await state.get_data()).get('contact_id')
    correct_relations = True
    text = phrases['phrases']['userAdded'][lang]

    if message.text != phrases['phrases']['addBirthday'][lang]:
        text = phrases['phrases']['userNotAdded'][lang]
        correct_relations = False

    if usr_id == contact_id:
        text = phrases['phrases']['addSelf'][lang]
        correct_relations = False

    if datasource.check_relationship(usr_id, contact_id):
        text = phrases['phrases']['alreadyFriend'][lang]
        correct_relations = False

    if correct_relations:
        datasource.add_relationship(usr_id, contact_id)

    await message.answer(text=text, reply_markup=main_keyboard())
    await state.clear()
