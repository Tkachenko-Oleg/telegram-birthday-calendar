from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.bot.services.tools import Tools

def days_keyboard(month):
    keyboard = ReplyKeyboardBuilder()
    for day in range(1, 33):
        if day <= Tools.max_day_of_month(month):
            keyboard.add(KeyboardButton(text=str(day)))
        else:
            keyboard.add(KeyboardButton(text='ᅠ'))
    keyboard.adjust(8)
    return keyboard.as_markup(resize_keyboard=True)
