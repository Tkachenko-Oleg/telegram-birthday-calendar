from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def options_keyboard(phrases, lang):
    texts = [
        phrases['phrases']['changeLanguage'][lang],
        phrases['phrases']['changeName'][lang],
        phrases['phrases']['changeBirthday'][lang],
        phrases['phrases']['Back'][lang]
    ]

    keyboard = ReplyKeyboardBuilder()
    for text in texts:
        keyboard.add(KeyboardButton(text=text))
    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)
