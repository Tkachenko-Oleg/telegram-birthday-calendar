from datetime import date


class Tools:
    @staticmethod
    def get_month_number(string_month: str, lang: str) -> int:
        months_en = [
            'January ❄️',
            'February ❄️',
            'March 🌱',
            'April 🌱',
            'May 🌱',
            'June ☀️',
            'July ☀️',
            'August ☀️',
            'September 🍁',
            'October 🍁',
            'november 🍁',
            'December ❄️'
        ]
        months_ru = [
            'Январь ❄️',
            'Февраль ❄️',
            'Март 🌱',
            'Апрель 🌱',
            'Май 🌱',
            'Июнь ☀️',
            'Июль ☀️',
            'Август ☀️',
            'Сентябрь 🍁',
            'Октябрь 🍁',
            'Ноябрь 🍁',
            'Декабрь ❄️'
        ]
        try:
            if lang == 'En':
                return months_en.index(string_month) + 1
            elif lang == 'Ru':
                return months_ru.index(string_month) + 1
        except ValueError:
            return 0



    @staticmethod
    def parse_postgres_date(data: str, lang: str) -> str:
        months_en = [
            'January ❄️',
            'February ❄️',
            'March 🌱',
            'April 🌱',
            'May 🌱',
            'June ☀️',
            'July ☀️',
            'August ☀️',
            'September 🍁',
            'October 🍁',
            'november 🍁',
            'December ❄️'
        ]
        months_ru = [
            'Январь ❄️',
            'Февраль ❄️',
            'Март 🌱',
            'Апрель 🌱',
            'Май 🌱',
            'Июнь ☀️',
            'Июль ☀️',
            'Август ☀️',
            'Сентябрь 🍁',
            'Октябрь 🍁',
            'Ноябрь 🍁',
            'Декабрь ❄️'
        ]
        date_list = data.split('-')
        month_index = int(date_list[1]) - 1
        day = int(date_list[2])
        if lang == '🇬🇧':
            month = months_en[month_index]
        elif lang == '🇷🇺':
            month = months_ru[month_index]
        else:
            month = 0
        return f"{day} {month}"


    @staticmethod
    def max_day_of_month(month: int) -> int:
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days_in_month[month-1]


    @staticmethod
    def correct_day(day: str, month: int) -> int:
        if day and day.isdigit() and (1 <= int(day) <= Tools.max_day_of_month(month)):
            return int(day)
        else:
            return 0


    @staticmethod
    def format_info_about_friend(data):
        data = str(data).replace('(', '').replace(')', '').split(',')
        name = data[0].replace('"', '')
        if data[1] == 'Ru':
            lang = "🇷🇺"
        elif data[1] == 'En':
            lang = "🇬🇧"
        else:
            lang = "🇬🇧"
        birth_date = Tools.parse_postgres_date(data[2], lang)
        phone_number = data[3]

        output_data = f"Name: {name}\n" \
                      f"Birthday 🎁: {birth_date}\n" \
                      f"Phone number ☎️: {phone_number}\n\n"

        return output_data


    @staticmethod
    def unpack_state_data(data: dict) -> dict:
        year = 2000
        month = int(data.get('birth_month'))
        day = int(data.get('birthday'))

        output_data = {
            "tg": data.get('tg_id'),
            "nick": data.get('nickname'),
            "name": data.get('name'),
            "lang": data.get('language'),
            "birth": date(year, month, day),
            "phone": data.get('phone_number')
        }

        return output_data


    @staticmethod
    def parse_postgres(data: tuple, phrases: dict, lang: str) -> str:
        data = str(data).replace('(', '').replace(')', '').split(',')

        nickname = data[0].replace('"', '')
        name = data[1].replace('"', '')
        phone_number = data[3]
        if data[4] == 'Ru':
            language = "🇷🇺"
        elif data[4] == 'En':
            language = "🇬🇧"
        else:
            language = "🇬🇧"
        birth_date = Tools.parse_postgres_date(data[2], language)

        out_string = f"{phrases['fields']['nick'][lang]}: {nickname}\n" \
                     f"{phrases['fields']['name'][lang]}: {name}\n" \
                     f"{phrases['fields']['birthday'][lang]}: {birth_date}\n" \
                     f"{phrases['fields']['phone'][lang]}: {phone_number}\n" \
                     f"{phrases['fields']['language'][lang]}: {language}"

        return out_string


    @staticmethod
    def is_correct_name_message(message: str) -> str:
        if message:
            if len(message) <= 50:
                return "correct message"
            else:
                return "long message"
        else:
            return "non-textual"


    @staticmethod
    def create_help_text(phrases, lang):
        text = f"{phrases['helpText']['showProfile'][lang]}\n\n" \
               f"{phrases['helpText']['changeProfile'][lang]}\n\n" \
               f"{phrases['helpText']['deleteProfile'][lang]}\n\n" \
               f"{phrases['helpText']['searchProfile'][lang]}\n\n" \
               f"{phrases['helpText']['showBirthdayList'][lang]}"
        return text
