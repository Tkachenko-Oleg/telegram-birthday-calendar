from .interface import InterfaceCommandLogic


class BotCommandLogic(InterfaceCommandLogic):
    def __init__(self):
        super().__init__()

    def get_all_birthdays(self, db: dict) -> str:
        output = list()
        # print(self)
        for i in db:
            output.append(f"{db[i]['name']}: "
                          f"{db[i]['birthday']['year']}."
                          f"{db[i]['birthday']['month']}."
                          f"{db[i]['birthday']['day']}")
        return "\n".join(output)

    def get_today_birthdays(self, db: dict) -> str:
        pass

    def add_new_birthday(self, db: dict, name: str, year: int, month: int, day: int) -> None:
        pass
