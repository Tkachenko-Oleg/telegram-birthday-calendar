from datetime import date

from .datasource import DataSource
from .user_model import UserModel


class IsMemoryDataSource(DataSource):
    __db:dict = dict()

    def get_all_birthdays(self, user_id: int):
        output = list()
        for element in self.__db:
            row = self.__db[element]
            if row['user_id'] == user_id:
                output.append(f"{row['name']}: {row['birthday']}")

        output = "\n".join(output)
        if output:
            return f"Your birthdays list: \n{output}"
        else:
            return "Your birthdays list is empty"

    def get_today_birthdays(self, user_id: int):
        output = list()
        today_date = date.today()

        for element in self.__db:
            row = self.__db[element]
            if row['user_id'] == user_id and row['birthday'] == today_date:
                output.append(f"{row['name']}: {row['birthday']}")

        output = "\n".join(output)
        if output:
            return f"Today birthdays:\n{output}"
        else:
            return "Today birthdays is not found"

    def add_new_birthday(self, data: dict, user_id: int):
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))

        user = UserModel()
        user.user_id = user_id
        user.name = data.get('name')
        user.birthday = date(year, month, day)

        key = len(self.__db)
        value = {'user_id': user_id, 'name': user.name, 'birthday': user.birthday}
        self.__db.update({key: value})

        return f"Your new data:\n{user.name}: {user.birthday}"
