from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def delete_friend_keyboard(phrases, lang):
    delete_buttons = [[
        KeyboardButton(text=phrases['phrases']['confirmationDeleteFriend'][lang]),
        KeyboardButton(text=phrases['phrases']['Back'][lang]),
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=delete_buttons, resize_keyboard=True)
    return keyboard
