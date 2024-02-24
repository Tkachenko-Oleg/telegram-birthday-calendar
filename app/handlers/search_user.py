from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.content_type import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F

from main import dp, datasource, phrases, panels, tools
from states import FormSearchUser


@dp.message(Command('search_user'))
async def method_for_search_contact_handler(message: Message, state :FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    if usr_id:
        lang = datasource.get_lang(usr_id)
        text = phrases['phrases']['searchMethod'][lang]
        await message.answer(text=text, reply_markup=panels.search_user_methods(usr_id, phrases, lang))
        await state.set_state(FormSearchUser.search_state)
    else:
        await message.answer("You are not registered")


@dp.message(FormSearchUser.search_state)
async def choose_method(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)
    content = message.content_type
    match content:
        case ContentType.USER_SHARED:
            contact_id = datasource.get_id(str(message.user_shared.user_id))
            if contact_id:
                postgres_data = datasource.user_profile(contact_id)
                contact_data = tools.parse_postgres(postgres_data)
                contact_info = f"{phrases['fields']['nick'][lang]}: {contact_data.get('nick')}\n" \
                       f"{phrases['fields']['name'][lang]}: {contact_data.get('name')}\n" \
                       f"{phrases['fields']['birthday'][lang]}: {contact_data.get('birth')}\n" \
                       f"{phrases['fields']['phone'][lang]}: {contact_data.get('phone')}\n" \
                       f"{phrases['fields']['language'][lang]}: {contact_data.get('lang')}"
                text = phrases['phrases']['questAddUser'][lang]
                await state.update_data(contact_id=contact_id)
                await message.answer(text=contact_info, reply_markup=panels.remove_panel())
                await message.answer(text=text, reply_markup=panels.add_contact(phrases, lang))
                await state.set_state(FormSearchUser.add_state)
            else:
                text = phrases['phrases']['userNotFound'][lang]
                await message.answer(text=text, reply_markup=panels.remove_panel())
                await state.clear()
        case ContentType.TEXT:
            if message.text == phrases['phrases']['searchNick'][lang]:
                text = phrases['phrases']['enterNickname'][lang]
                await message.answer(text=text, reply_markup=panels.remove_panel())
                await state.set_state(FormSearchUser.nickname_state)
            else:
                text = phrases['phrases']['noMethod'][lang]
                await message.answer(text=text, reply_markup=panels.commands_panel())
                await state.clear()
        case _:
            text = phrases['phrases']['noMethod'][lang]
            await message.answer(text=text, reply_markup=panels.commands_panel())
            await state.clear()


@dp.message(FormSearchUser.nickname_state)
async def search_nickname_contact(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    lang = datasource.get_lang(usr_id)
    nickname = message.text
    if datasource.is_nickname_exist(nickname):
        contact_id = datasource.get_id_by_nickname(nickname)
        postgres_data = datasource.user_profile(contact_id)
        contact_data = tools.parse_postgres(postgres_data)
        contact_info = f"{phrases['fields']['nick'][lang]}: {contact_data.get('nick')}\n" \
                       f"{phrases['fields']['name'][lang]}: {contact_data.get('name')}\n" \
                       f"{phrases['fields']['birthday'][lang]}: {contact_data.get('birth')}\n" \
                       f"{phrases['fields']['phone'][lang]}: {contact_data.get('phone')}\n" \
                       f"{phrases['fields']['language'][lang]}: {contact_data.get('lang')}"
        text = phrases['phrases']['questAddUser'][lang]
        await state.update_data(contact_id=contact_id)
        await message.answer(text=contact_info, reply_markup=panels.remove_panel())
        await message.answer(text=text, reply_markup=panels.add_contact(phrases, lang))
        await state.set_state(FormSearchUser.add_state)
    else:
        text = phrases['phrases']['userNotFound'][lang]
        await message.answer(text=text, reply_markup=panels.remove_panel())
        await state.clear()


@dp.message(FormSearchUser.add_state)
async def add_contact(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    usr_id = datasource.get_id(tg_id)
    contact_id = dict(await state.get_data()).get('contact_id')
    lang = datasource.get_lang(usr_id)

    if message.text == phrases['phrases']['addBirthday'][lang]:
        if usr_id != contact_id:
            if not datasource.check_relationship(usr_id, contact_id):
                text = phrases['phrases']['userAdded'][lang]
                datasource.check_relationship(usr_id, contact_id)
                datasource.add_relationship(usr_id, contact_id)
            else:
                text = phrases['phrases']['alreadyFriend'][lang]
        else:
            text = phrases['phrases']['addSelf'][lang]
    else:
        text = phrases['phrases']['userNotAdded'][lang]
    await message.answer(text=text, reply_markup=panels.commands_panel())
    await state.clear()
