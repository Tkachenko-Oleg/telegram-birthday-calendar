from datetime import datetime, date

class Tools:
    @staticmethod
    def check_correct_data(year: str = '0001', month: str = '01', day: str = '01'):
        try:
            if len(year) < 4:
                year = ('0' * (4 - len(year))) + year
            if len(month) < 2:
                month = '0' + month
            if len(day) < 2:
                day = '0' + day

            if int(year) <= datetime.now().year:
                date.fromisoformat(f"{year}-{month}-{day}")
                return True
            else:
                raise ValueError

        except ValueError:
            return False
