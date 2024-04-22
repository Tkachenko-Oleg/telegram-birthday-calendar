from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def friend_keyboard(phrases, lang):
    friends_buttons = [[
        KeyboardButton(text=phrases['phrases']['addFriend'][lang]),
        KeyboardButton(text=phrases['phrases']['infoAboutFriend'][lang]),
        KeyboardButton(text=phrases['phrases']['Back'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=friends_buttons, resize_keyboard=True)
    return keyboard
