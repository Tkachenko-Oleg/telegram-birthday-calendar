from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def info_keyboard(phrases, lang):
    buttons = [[
        KeyboardButton(text=phrases['phrases']['deleteFriend'][lang]),
        KeyboardButton(text=phrases['phrases']['Back'][lang]),
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
