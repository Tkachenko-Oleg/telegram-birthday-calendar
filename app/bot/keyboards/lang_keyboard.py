from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def language_keyboard():
    lang_buttons = [[KeyboardButton(text='Русский 🇷🇺'), KeyboardButton(text='English 🇬🇧')]]
    keyboard = ReplyKeyboardMarkup(keyboard=lang_buttons, resize_keyboard=True)
    return keyboard
