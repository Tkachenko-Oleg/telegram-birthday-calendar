from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRequestUser, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from .tools import Tools


class Panels:
    @staticmethod
    def remove_panel():
        return ReplyKeyboardRemove()


    @staticmethod
    def language_panel():
        lang_buttons = [[KeyboardButton(text='Русский 🇷🇺'), KeyboardButton(text='English 🇬🇧')]]
        panel = ReplyKeyboardMarkup(keyboard=lang_buttons, resize_keyboard=True)
        return panel


    @staticmethod
    def contact_panel(phrases, lang):
        text = phrases['phrases']['registration'][lang]
        button_contact = [[KeyboardButton(text=text, request_contact=True)]]
        panel = ReplyKeyboardMarkup(keyboard=button_contact, resize_keyboard=True)
        return panel


    @staticmethod
    def month_panel(phrases, lang):
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


    @staticmethod
    def day_panel(month):
        builder_day = ReplyKeyboardBuilder()
        for day in range(1, 33):
            if day <= Tools.max_day_of_month(month):
                builder_day.add(KeyboardButton(text=str(day)))
            else:
                builder_day.add(KeyboardButton(text='ᅠ'))
        builder_day.adjust(8)
        return builder_day.as_markup(resize_keyboard=True)


    @staticmethod
    def commands_panel():
        command_buttons = [
            [KeyboardButton(text='/help')],
            [KeyboardButton(text='/my_profile')],
            [KeyboardButton(text='/change_profile')],
            [KeyboardButton(text='/delete_profile')],
            [KeyboardButton(text='/search_user')],
            [KeyboardButton(text='/show_my_birthday_list')]
        ]
        commands_panel = ReplyKeyboardMarkup(keyboard=command_buttons)
        return commands_panel


    @staticmethod
    def changes_panel(phrases, lang):
        change_buttons = [[
            KeyboardButton(text=phrases['phrases']['changeLanguage'][lang]),
            KeyboardButton(text=phrases['phrases']['changeName'][lang]),
            KeyboardButton(text=phrases['phrases']['changeBirthday'][lang])
        ]]
        panel = ReplyKeyboardMarkup(keyboard=change_buttons, resize_keyboard=True)
        return panel


    @staticmethod
    def delete_profile(phrases, lang):
        delete_button = [[
            KeyboardButton(text=phrases['phrases']['questDelProfile'][lang]),
            KeyboardButton(text=phrases['phrases']['questNotDelProfile'][lang])
        ]]
        panel = ReplyKeyboardMarkup(keyboard=delete_button, resize_keyboard=True)
        return panel


    @staticmethod
    def search_user_methods(request_id, phrases, lang):
        method_buttons = [[
            KeyboardButton(text=phrases['phrases']['searchContact'][lang],
                request_user=KeyboardButtonRequestUser(request_id=request_id, user_is_bot=False)),
            KeyboardButton(text=phrases['phrases']['searchNick'][lang])
        ]]
        panel = ReplyKeyboardMarkup(keyboard=method_buttons, resize_keyboard=True)
        return panel


    @staticmethod
    def add_contact(phrases, lang):
        add_buttons = [[
            KeyboardButton(text=phrases['phrases']['addBirthday'][lang]),
            KeyboardButton(text=phrases['phrases']['notAddBirthday'][lang])
        ]]
        panel = ReplyKeyboardMarkup(keyboard=add_buttons, resize_keyboard=True)
        return panel
