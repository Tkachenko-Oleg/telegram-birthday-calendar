from aiogram.fsm.state import State, StatesGroup

class FriendsState(StatesGroup):
    friends_is_active = State()

    search_method = State()
    add_state = State()
    nickname_state = State()

    friend_info = State()

    delete_nickname = State()
    delete_state = State()
