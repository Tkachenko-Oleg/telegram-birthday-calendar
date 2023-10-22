from datetime import datetime

from .interface import InterfaceCommandLogic


class BotCommandLogic(InterfaceCommandLogic):
    @classmethod
    def get_all_birthdays(cls, db: dict) -> str:
        output = list()

        for element in db:
            row = db[element]['birthday']
            output.append(f"{db[element]['name']}: "
                          f"{row['year']}."
                          f"{row['month']}."
                          f"{row['day']}")

        return "\n".join(output)

    @classmethod
    def get_today_birthdays(cls, db: dict) -> str:
        output = list()
        time_now = str(datetime.date(datetime.now())).replace('-', '.')

        for element in db:
            row = db[element]['birthday']
            string = f"{row['year']}.{row['month']}.{row['day']}"

            if string == time_now:
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
    def add_new_birthday(cls, db: dict, data: dict) -> str:
        key = len(db)
        value = {'name': data.get('name'),
                 'birthday': {'year': data.get('year'),
                              'month': data.get('month'),
                              'day': data.get('day')}}

        db.update({key: value})

        return f"Your new data:\n" \
               f"{data.get('name')}: " \
               f"{data.get('year')}.{data.get('month')}.{data.get('day')}"
