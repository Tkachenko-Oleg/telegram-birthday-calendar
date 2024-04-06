from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def delete_profile(phrases, lang):
    delete_button = [[
        KeyboardButton(text=phrases['phrases']['questDelProfile'][lang]),
        KeyboardButton(text=phrases['phrases']['questNotDelProfile'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=delete_button, resize_keyboard=True)
    return keyboard
