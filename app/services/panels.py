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
            [KeyboardButton(text='/show_my_profile')],
            [KeyboardButton(text='/change_my_profile')],
            [KeyboardButton(text='/delete_my_profile')],
            [KeyboardButton(text='/search_user')],
            [KeyboardButton(text='/show_my_birthday_list')]
        ]
        commands_panel = ReplyKeyboardMarkup(keyboard=command_buttons)
        return commands_panel


    # @staticmethod
    # def changes_panel():
    #     button_changes = [[
    #         KeyboardButton(text='change language'),
    #         KeyboardButton(text='change name'),
    #         KeyboardButton(text='change birthday')
    #     ]]
    #     panel = ReplyKeyboardMarkup(keyboard=button_changes, resize_keyboard=True)
    #     return panel
    #
    #
    # @staticmethod
    # def change_language_panel():
    #     button_lang = [[KeyboardButton(text='Ру 🇷🇺'), KeyboardButton(text='En 🇬🇧')]]
    #     panel = ReplyKeyboardMarkup(keyboard=button_lang, resize_keyboard=True)
    #     return panel
    #
    #
    # @staticmethod
    # def delete_profile():
    #     button_delete = [[KeyboardButton(text='delete profile ✅'), KeyboardButton(text='do not delete profile ❌')]]
    #     panel = ReplyKeyboardMarkup(keyboard=button_delete, resize_keyboard=True)
    #     return panel
    #
    #
    # @staticmethod
    # def search_user_methods(request_id: int):
    #     buttons = [[KeyboardButton(text='search with contact',
    #                               request_user=KeyboardButtonRequestUser(request_id=request_id, user_is_bot=False)),
    #                KeyboardButton(text='search with nickname')]]
    #     panel = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    #     return panel
    #
    #
    # @staticmethod
    # def add_contact():
    #     buttons = [[KeyboardButton(text="add birthday in my list ✅"),
    #                 KeyboardButton(text="don't add birthday ❌")]]
    #     panel = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    #     return panel
