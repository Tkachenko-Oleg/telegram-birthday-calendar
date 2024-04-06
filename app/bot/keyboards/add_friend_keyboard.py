from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def add_contact(phrases, lang):
    add_buttons = [[
        KeyboardButton(text=phrases['phrases']['addBirthday'][lang]),
        KeyboardButton(text=phrases['phrases']['notAddBirthday'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=add_buttons, resize_keyboard=True)
    return keyboard
