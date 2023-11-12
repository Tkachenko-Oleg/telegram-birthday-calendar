from datetime import date

from .datasource import DataSource
from .user_model import UserModel


class IsMemoryDataSource(DataSource):
    __db_users:dict = dict()
    __db_relation:dict = dict()

    def add_user_to_main_database(self, data):
        year = int(data.get('year_of_birth'))
        month = int(data.get('month_of_birth'))
        day = int(data.get('day_of_birth'))

        user = UserModel()
        user.tg_id = data.get('tg_id')
        user.username = data.get('username')
        user.nickname = data.get('nickname')
        user.phone_number = data.get('phone_number')
        user.language = data.get('language')
        user.birth_date = date(year, month, day)

        key = len(self.__db_users)
        value = {
            'unique_id': user.tg_id,
            'user_id': user.tg_id,
            'username': user.username,
            'nickname': user.nickname,
            'phone_number': user.phone_number,
            'language': user.language,
            'birth_date': user.birth_date
        }
        self.__db_users.update({key: value})

    def check_exist_user(self, tg_id):
        for element in self.__db_users:
            if tg_id == self.__db_users.get(element).get('user_id'):
                return True
        return False

    def show_user_profile(self, tg_id):
        for element in self.__db_users:
            if tg_id == self.__db_users.get(element).get('user_id'):
                data = self.__db_users.get(element)
                output_string = f"Nickname: {data.get('nickname')}\n" \
                                f"Phone number: {data.get('phone_number')}\n" \
                                f"Username: {data.get('username')}\n" \
                                f"Language: {data.get('language')}\n" \
                                f"Birth date: {data.get('birth_date')}"
                return output_string
        return None

    def delete_profile(self, tg_id):
        for element in self.__db_users:
            if tg_id == self.__db_users.get(element).get('user_id'):
                self.__db_users.pop(element)
                break

    def change_user_profile(self, tg_id, type_data, changed_data):
        for element in self.__db_users:
            if tg_id == self.__db_users.get(element).get('user_id'):
                if type(changed_data) == dict:
                    year = int(changed_data.get('year_of_birth'))
                    month = int(changed_data.get('month_of_birth'))
                    day = int(changed_data.get('day_of_birth'))
                    changed_data = date(year, month, day)
                self.__db_users.get(element)[type_data] = changed_data

    def search_user_by_nickname(self, nickname):
        for element in self.__db_users:
            if nickname == self.__db_users.get(element).get('nickname'):
                data = self.__db_users.get(element)
                output_string = f"Nickname: {data.get('nickname')}\n" \
                                f"Phone number: {data.get('phone_number')}\n" \
                                f"Username: {data.get('username')}\n" \
                                f"Birth date: {data.get('birth_date')}"
                return output_string, data.get('unique_id')
        return None, None

    def search_user_by_phone_number(self, phone_number):
        for element in self.__db_users:
            if phone_number == self.__db_users.get(element).get('phone_number'):
                data = self.__db_users.get(element)
                output_string = f"Nickname: {data.get('nickname')}\n" \
                                f"Phone number: {data.get('phone_number')}\n" \
                                f"Username: {data.get('username')}\n" \
                                f"Birth date: {data.get('birth_date')}"
                return output_string, data.get('unique_id')
        return None, None

    def check_the_relationship_database(self, tg_id, user_id_to_add):
        for element in self.__db_relation:
            if tg_id == self.__db_relation.get(element).get('main_user') and \
                    user_id_to_add == self.__db_relation.get(element).get('dependent_user'):
                return False
        return True

    def add_user_birthday_to_relation_database(self, tg_id, user_id_to_add):
        value_1 = None
        value_2 = None

        for element in self.__db_users:
            if tg_id == self.__db_users.get(element).get('user_id'):
                value_1 = self.__db_users.get(element).get('unique_id')

        if value_1:
            for element in self.__db_users:
                if user_id_to_add == self.__db_users.get(element).get('unique_id'):
                    value_2 = self.__db_users.get(element).get('unique_id')

            if value_2:
                user_key = len(self.__db_relation)
                user_value = {'main_user': value_1, 'dependent_user': value_2}
                self.__db_relation.update({user_key: user_value})
                return True
            else:
                return False
        else:
            return False

    def show_list_of_birthdays(self, tg_id):
        required_ids = list()
        list_of_birthdays = list()

        for element in self.__db_relation:
            if tg_id == self.__db_relation.get(element).get('main_user'):
                required_ids.append(self.__db_relation.get(element).get('dependent_user'))

        if required_ids:
            for user in required_ids:
                for element in self.__db_users:
                    if user == self.__db_users.get(element).get('unique_id'):
                        list_of_birthdays.append(f"Nickname: {self.__db_users.get(element).get('nickname')}\n"
                                                 f"Name: {self.__db_users.get(element).get('username')}\n"
                                                 f"Phone number: {self.__db_users.get(element).get('phone_number')}\n"
                                                 f"Birth date: {self.__db_users.get(element).get('birth_date')}\n")
            output_string = '\n'.join(list_of_birthdays)
            return output_string
        else:
            return 'Your birthday list is empty'
