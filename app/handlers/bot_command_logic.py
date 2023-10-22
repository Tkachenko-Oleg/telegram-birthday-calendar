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
    def add_new_birthday(cls, db: dict, name: str, year: int, month: int, day: int) -> None:
        pass
