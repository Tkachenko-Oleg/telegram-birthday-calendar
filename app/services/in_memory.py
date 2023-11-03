from datetime import datetime, date

from .datasource import DataSource
from .user_model import UserModel


class IsMemeryDataSource(DataSource):
    __db:dict = dict()
    def get_all_birthdays(self, user_id: str):
        output = list()

        for element in self.__db:
            if self.__db[element]['user_id'] == user_id:
                row = self.__db[element]['birthday']
                output.append(f"{self.__db[element]['name']}: "
                              f"{row['year']}."
                              f"{row['month']}."
                              f"{row['day']}")

        output_string = "\n".join(output)
        if output_string:
            return f"Your birthdays list: \n{output_string}"
        else:
            return "Your birthdays list is empty"

    def get_today_birthdays(self, user_id: str):
        output = list()
        time_now = str(datetime.date(datetime.now())).replace('-', '.')

        for element in self.__db:
            row = self.__db[element]['birthday']
            date_string = f"{row['year']}.{row['month']}.{row['day']}"

            if self.__db[element]['user_id'] == user_id and date_string == time_now:
                output.append(f"{self.__db[element]['name']}: "
                              f"{row['year']}."
                              f"{row['month']}."
                              f"{row['day']}")

        output_string = "\n".join(output)
        if output_string:
            return f"Today birthdays:\n{output_string}"
        else:
            return "Today birthdays is not found"

    def add_new_birthday(self, data: dict, user_id: str):
        user = UserModel()
        # user.user_id = user_id
        # user.birthday = data

        key = len(self.__db)
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        if len(data.get('month')) < 2:
            month = '0' + month
        if len(data.get('day')) < 2:
            day = '0' + day

        value = {'user_id': user_id,
                 'name': data.get('name'),
                 'birthday': {'year': year,
                              'month': month,
                              'day': day}}

        self.__db.update({key: value})

        # return user.birthday

        return f"Your new data:\n" \
               f"{data.get('name')}: " \
               f"{data.get('year')}.{data.get('month')}.{data.get('day')}"
