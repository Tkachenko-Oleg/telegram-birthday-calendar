from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRequestUser

def search_user_methods(request_id, phrases, lang):
    method_buttons = [[
        KeyboardButton(text=phrases['phrases']['searchContact'][lang],
                       request_user=KeyboardButtonRequestUser(request_id=request_id, user_is_bot=False)),
        KeyboardButton(text=phrases['phrases']['searchNick'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=method_buttons, resize_keyboard=True)
    return keyboard
