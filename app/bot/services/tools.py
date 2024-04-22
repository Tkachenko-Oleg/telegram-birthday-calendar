from datetime import date, datetime


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
        if lang == '🇬🇧' or lang == 'En':
            month = months_en[month_index]
        elif lang == '🇷🇺' or lang == 'Ru':
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
        month = int(data.get('month'))
        day = int(data.get('day'))

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
    def correct_chars(message):
        correct_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                         'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                         'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                         'Y', 'Z', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж',
                         'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
                         'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ',
                         'ы', 'ь', 'э', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д',
                         'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н',
                         'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч',
                         'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '0', '1',
                         '2', '3', '4', '5', '6', '7', '8', '9', '_']
        for char in message:
            if char not in correct_chars:
                return False
        return True



    @staticmethod
    def is_correct_name_message(message: str, phrases: dict, lang: str) -> str:
        if not message:
            return phrases['phrases']['textMessage'][lang]
        if ' ' in message:
            return phrases['phrases']['spaceInMessage'][lang]
        if not Tools.correct_chars(message):
            return phrases['phrases']['incorrectChars'][lang]
        if len(message) > 50:
            return phrases['phrases']['longMessage'][lang]
        return "correct message"


    @staticmethod
    def create_help_text(phrases, lang):
        text = f"{phrases['helpText']['showProfile'][lang]}\n\n" \
               f"{phrases['helpText']['changeProfile'][lang]}\n\n" \
               f"{phrases['helpText']['deleteProfile'][lang]}\n\n" \
               f"{phrases['helpText']['searchProfile'][lang]}\n\n" \
               f"{phrases['helpText']['showBirthdayList'][lang]}"
        return text


    @staticmethod
    def convert_postgres_birthdays_list_to_string(postgres_string, phrases, lang):
        string = f"{phrases['phrases']['friendsTitle'][lang]}\n"
        friends_list = list()
        friend_number = 0

        for element in postgres_string:
            element = element[0].replace('(', '').replace(')', '').split(',')
            friends_list.append({'nickname': element[0], 'date': element[1]})

        sorted_friends_list = sorted(friends_list, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        for element in sorted_friends_list:
            friend_number += 1
            string += f"{friend_number}) {element['nickname']} - {Tools.parse_postgres_date(element['date'], lang)}\n"
        return string


























































