from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def registration_keyboard(phrases, lang):
    text = phrases['phrases']['registration'][lang]
    button_contact = [[KeyboardButton(text=text, request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=button_contact, resize_keyboard=True)
    return keyboard
