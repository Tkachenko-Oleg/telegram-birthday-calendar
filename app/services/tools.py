from datetime import date, datetime

class Tools:
    @staticmethod
    def check_correct_data(input_date: dict):
        year = input_date.get('year_of_birth')
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
    def parse_postgres_string(postgres_string):
        data = str(postgres_string).replace('(', '').replace(')', '').split(',')
        data_string = f"Nickname: {data[1]}\n" \
                      f"Username: {data[2]}\n" \
                      f"Birth date: {data[3]}\n" \
                      f"Phone number: {data[4]}\n" \
                      f"Language: {data[5]}"
        return data_string


    @staticmethod
    def parse_postgres_id(data_string):
        data = str(data_string).replace('(', '').replace(')', '').split(',')
        return data[0]


    @staticmethod
    def make_date_string(date_string):
        year = int(date_string.get('year_of_birth'))
        month = int(date_string.get('month_of_birth'))
        day = int(date_string.get('day_of_birth'))
        return date(year, month, day)
