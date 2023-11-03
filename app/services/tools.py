from datetime import datetime

class Tools:
    @staticmethod
    def check_correct_data(input_date: dict):
        year = input_date.get('year')
        month = input_date.get('month')
        day = input_date.get('day')

        try:
            if int(year) < 1800:
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
