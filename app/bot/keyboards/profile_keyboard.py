from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def profile(phrases, lang):
    profile_buttons = [[
        KeyboardButton(text=phrases['phrases']['profileChange'][lang]),
        KeyboardButton(text=phrases['phrases']['profileDelete'][lang]),
        KeyboardButton(text=phrases['phrases']['Back'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=profile_buttons, resize_keyboard=True)
    return keyboard
