from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRequestUser

def search_keyboard(request_id, phrases, lang):
    method_buttons = [[
        KeyboardButton(text=phrases['phrases']['searchContact'][lang],
                       request_user=KeyboardButtonRequestUser(request_id=request_id, user_is_bot=False)),
        KeyboardButton(text=phrases['phrases']['searchNick'][lang]),
        KeyboardButton(text=phrases['phrases']['Back'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=method_buttons, resize_keyboard=True)
    return keyboard
