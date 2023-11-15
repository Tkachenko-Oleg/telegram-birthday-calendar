class DataSource:
    def add_user_to_main_database(self, data):
        pass

    def check_exist_user(self, tg_id):
        pass

    def check_exist_nickname(self, nickname):
        pass

    def show_user_profile(self, tg_id):
        pass

    def delete_profile(self, tg_id):
        pass

    def change_user_profile(self, tg_id, type_data, changed_data):
        pass

    def search_user_by_nickname(self, nickname):
        pass

    def search_user_by_phone_number(self, phone_number):
        pass

    def check_the_relationship_database(self, tg_id, unique_id):
        pass

    def add_user_birthday_to_relation_database(self, tg_id, unique_id):
        pass

    def show_list_of_birthdays(self, tg_id):
        pass
