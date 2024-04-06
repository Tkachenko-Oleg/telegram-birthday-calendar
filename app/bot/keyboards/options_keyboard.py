from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def options_keyboard(phrases, lang):
    change_buttons = [[
        KeyboardButton(text=phrases['phrases']['changeLanguage'][lang]),
        KeyboardButton(text=phrases['phrases']['changeName'][lang]),
        KeyboardButton(text=phrases['phrases']['changeBirthday'][lang])
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=change_buttons, resize_keyboard=True)
    return keyboard
