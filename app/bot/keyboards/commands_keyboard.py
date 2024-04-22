from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_keyboard():
    command_buttons = [
        [KeyboardButton(text='/help')],
        [KeyboardButton(text='/profile')],
        [KeyboardButton(text='/friends')],
        [KeyboardButton(text='/wishes')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=command_buttons)
    return keyboard
