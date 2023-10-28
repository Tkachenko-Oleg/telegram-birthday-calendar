from datetime import datetime, date

from .interface import InterfaceCommandLogic


class BotCommandLogic(InterfaceCommandLogic):
    @classmethod
    def get_all_birthdays(cls, db: dict, user_id: str) -> str:
        output = list()

        for element in db:
            if db[element]['user_id'] == user_id:
                row = db[element]['birthday']
                output.append(f"{db[element]['name']}: "
                              f"{row['year']}."
                              f"{row['month']}."
                              f"{row['day']}")

        return "\n".join(output)

    @classmethod
    def get_today_birthdays(cls, db: dict, user_id: str) -> str:
        output = list()
        time_now = str(datetime.date(datetime.now())).replace('-', '.')

        for element in db:
            row = db[element]['birthday']
            string = f"{row['year']}.{row['month']}.{row['day']}"

            if db[element]['user_id'] == user_id and string == time_now:
                output.append(f"{db[element]['name']}: "
                              f"{row['year']}."
                              f"{row['month']}."
                              f"{row['day']}")

        output_string = "\n".join(output)
        if output_string:
            return f"Today birthdays:\n{output_string}"
        else:
            return "Today birthdays is not found"

    @classmethod
    def add_new_birthday(cls, db: dict, data: dict, user_id: str) -> str:
        key = len(db)
        value = {'user_id': user_id,
                 'name': data.get('name'),
                 'birthday': {'year': data.get('year'),
                              'month': data.get('month'),
                              'day': data.get('day')}}

        db.update({key: value})

        return f"Your new data:\n" \
               f"{data.get('name')}: " \
               f"{data.get('year')}.{data.get('month')}.{data.get('day')}"

    @classmethod
    def check_correct_data(cls, year: str = '0001',
                           month: str = '01',
                           day: str = '01') -> bool:
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
