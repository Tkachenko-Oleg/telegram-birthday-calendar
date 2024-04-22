from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def months_keyboard(phrases, lang):
    month_key = [
        "december",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november"
    ]
    months = list(phrases['months'][key][lang] for key in month_key)
    builder_month = ReplyKeyboardBuilder()
    for month in months:
        builder_month.add(KeyboardButton(text=month))
    builder_month.adjust(3)
    return builder_month.as_markup(resize_keyboard=True)
