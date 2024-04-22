from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def delete_profile_keyboard(phrases, lang):
    delete_button = [[
        KeyboardButton(text=phrases['phrases']['questDelProfile'][lang]),
        KeyboardButton(text=phrases['phrases']['Back'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=delete_button, resize_keyboard=True)
    return keyboard
