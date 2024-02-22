from datetime import date, datetime

class Tools:
    @staticmethod
    def check_correct_data(input_date: dict):
        year = 2000
        month = input_date.get('month_of_birth')
        day = input_date.get('day_of_birth')

        try:
            if int(year) < 1800 or date.today().year < int(year) + 1:
                return False
            if not month:
                month = '01'
            if not day:
                day = '01'

            if datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d"):
                return True
            else:
                raise ValueError
        except ValueError:
            return False


    @staticmethod
    def parse_postgres_string_data(postgres_string: str) -> str:
        del_char = '"'
        data = str(postgres_string).replace('(', '').replace(')', '').split(',')

        nickname = data[0].replace(del_char, '')
        username = data[1].replace(del_char, '')
        phone_number = data[3]
        language = data[4]
        birth_date = Tools.convert_postgres_date_to_tg_date(data[2])

        answer_string = f"Nickname: {nickname}\n" \
                        f"Username: {username}\n" \
                        f"Language: {language}\n" \
                        f"Birthday: {birth_date}\n" \
                        f"Phone number: {phone_number}"

        return answer_string


    @staticmethod
    def parse_postgres_id(data_string):
        data = str(data_string).replace('(', '').replace(')', '').split(',')
        return data[0]


    @staticmethod
    def make_date_string(date_string):
        month = int(date_string.get('month_of_birth'))
        day = int(date_string.get('day_of_birth'))
        return date(2000, month, day)


    @staticmethod
    def convert_string_to_integer_month(string_month: str) -> int | bool:
        months = [
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
        try:
            integer_month = months.index(string_month) + 1
            return integer_month
        except ValueError:
            return False


    @staticmethod
    def convert_postgres_date_to_tg_date(data: str) -> str:
        months = [
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

        date_list = data.split('-')
        month_index = int(date_list[1]) - 1
        day = int(date_list[2])

        answer_date = f"{day} {months[month_index]}"

        return answer_date


    @staticmethod
    def max_day_of_month(month: int) -> int:
        list_31 = [1, 3, 5, 7, 8, 10, 12]
        list_30 = [4, 6, 9, 11]
        if month in list_31:
            return 31
        elif month in list_30:
            return 30
        else:
            return 29


    @staticmethod
    def correct_day(day: str) -> int | bool:
        if day and (1 <= int(day) <= 31):
            return int(day)
        else:
            return False


    @staticmethod
    def format_relations_birthdays(data):
        return list(int(''.join(map(str,friend_id))) for friend_id in data)


    @staticmethod
    def format_info_about_friend(data):
        del_char = '"'
        data = str(data).replace('(', '').replace(')', '').split(',')

        username = data[0].replace(del_char, '')
        phone_number = data[1]
        birth_date = Tools.convert_postgres_date_to_tg_date(data[2])

        answer_string = f"Nick: {username}\n" \
                        f"Phone number ☎️: {phone_number}\n" \
                        f"Birthday 🎁: {birth_date}\n"

        return answer_string

