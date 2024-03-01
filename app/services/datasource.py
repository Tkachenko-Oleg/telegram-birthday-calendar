class DataSource:
    def get_id(self, tg_id: int) -> int:
        pass

    def is_user_exist(self, tg_id: int) -> bool:
        pass

    def is_nickname_exist(self, nickname: str) -> bool:
        pass

    def add_new_user(self, tg_id: int, data: dict) -> None:
        pass

    def get_lang(self, tg_id: int) -> str:
        pass

    def user_profile(self, tg_id: int) -> tuple:
        pass

    def change_language(self, tg_id: int, lang: str) -> None:
        pass

    def change_name(self, tg_id: int, name: str) -> None:
        pass

    def change_birthday(self, tg_id: int, birth_month: int, birthday: int) -> None:
        pass

    def delete_profile(self, tg_id: int) -> None:
        pass

    def check_relationship(self, usr_id: int, contact_id: int) -> bool:
        pass

    def add_relationship(self, usr_id: int, contact_id: int) -> None:
        pass

    def get_id_by_nickname(self, nickname: str) -> int:
        pass

    def get_relationship_ids(self, usr_id: int) -> list:
        pass

    def get_birthday(self, usr_id: int) -> tuple:
        pass
