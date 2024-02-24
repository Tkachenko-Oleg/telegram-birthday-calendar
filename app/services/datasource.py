class DataSource:
    def get_id(self, tg_id: str) -> int:
        pass

    def is_nickname_exist(self, nickname: str) -> bool:
        pass

    def add_new_user_id(self, tg_id: str) -> None:
        pass

    def add_new_user_info(self, usr_id: int, data: dict) -> None:
        pass

    def get_lang(self, usr_id: int) -> str:
        pass

    def user_profile(self, usr_id: int) -> tuple:
        pass

    def change_language(self, usr_id: int, lang: str) -> None:
        pass

    def change_name(self, usr_id: int, name: str) -> None:
        pass

    def change_birthday(self, usr_id: int, birth_month: int, birthday: int) -> None:
        pass

    def delete_profile(self, usr_id: int):
        pass

    def check_relationship(self, usr_id: int, contact_id: int):
        pass

    def add_relationship(self, usr_id: int, contact_id: int):
        pass

    def get_id_by_nickname(self, nickname: str):
        pass























    def add_user_to_main_database(self, data):
        pass

    def check_exist_user(self, tg_id):
        pass

    def check_exist_nickname(self, nickname):
        pass

    def show_user_profile(self, tg_id):
        pass

    # def delete_profile(self, user_id):
    #     pass

    def change_user_profile(self, tg_id, type_data, changed_data):
        pass

    def search_user_by_nickname(self, nickname):
        pass

    def search_user_by_contact_id(self, tg_id):
        pass

    def search_user_info(self, tg_id, nickname):
        pass

    def search_user_id_info(self, tg_id, nickname):
        pass

    def search_contact(self, tg_id, nickname):
        pass

    def search_contact_info(self, tg_id=None, nickname=None):
        pass

    def check_the_relationship_database(self, tg_id, unique_id):
        pass

    def add_user_birthday_to_relation_database(self, user_id, contact_id):
        pass

    def show_list_of_birthdays(self, user_id):
        pass

    def get_id_user(self, tg_id):
        pass

    def get_info_about_birthday(self, user_id):
        pass