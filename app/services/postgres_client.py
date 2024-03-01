import psycopg2

from .datasource import DataSource
from config import Config

class IsDataBaseSource(DataSource):
    def __init__(self):
        self.connect = psycopg2.connect(
            database=Config.database,
            user=Config.username,
            password=Config.password,
            host=Config.host,
            port=Config.port)
        self.cursor = self.connect.cursor()


    def create_table(self):
        with self.connect:
            self.cursor.execute(
                """
                create type UserLang as Enum (
                'Ru',
                'En'
                )
                """
            )

            self.cursor.execute(
                """
                create table if not exists tg_users
                (
                    user_id bigserial not null primary key,
                    tg_id bigint not null unique,
                    user_nickname varchar(50) not null unique,
                    user_name varchar(50),
                    language UserLang,
                    birth_date date not null,
                    phone_number varchar(20) not null unique
                );
                """
            )

            self.cursor.execute(
                """
                create table if not exists user_relations
                (
                    user_id bigint not null references tg_users (user_id) on delete cascade,
                    friend_id bigint not null references tg_users (user_id) on delete cascade,
                    unique (user_id, friend_id)
                );
                """
            )

            self.connect.commit()


    def get_id(self, tg_id: int) -> int:
        with self.connect:
            self.cursor.execute(
                """
                select user_id
                from tg_users
                where tg_id = %s
                """,
                (tg_id,)
            )
        data = self.cursor.fetchone()
        if data:
            return data[0]
        return 0


    def is_user_exist(self, tg_id: int) -> bool:
        with self.connect:
            self.cursor.execute(
                """
                select exists (
                select 1
                from tg_users
                where tg_id = %s
                );
                """,
                (tg_id,)
            )
        data = self.cursor.fetchone()[0]
        return data


    def is_nickname_exist(self, nickname: str) -> bool:
        with self.connect:
            self.cursor.execute(
                """
                select exists (
                select 1
                from tg_users
                where user_nickname = %s
                );
                """,
                (nickname,)
            )
        data = self.cursor.fetchone()[0]
        return data


    def add_new_user(self, tg_id: int, data: dict) -> None:
        with self.connect:
            self.cursor.execute(
                """
                insert into tg_users
                (tg_id, user_nickname, user_name, language, birth_date, phone_number)
                values (%s, %s, %s, %s, %s, %s);
                """,
                (tg_id, data.get('nick'), data.get('name'), data.get('lang'), data.get('birth'), data.get('phone'))
            )
            self.connect.commit()


    def get_lang(self, tg_id: int) -> str:
        with self.connect:
            self.cursor.execute(
                """
                select language
                from tg_users
                where tg_id = %s
                """,
                (tg_id,)
            )

            lang = self.cursor.fetchone()[0]
            return lang


    def user_profile(self, tg_id: int) -> tuple:
        with self.connect:
            self.cursor.execute(
                """
                select (user_nickname, user_name, birth_date, phone_number, language)
                from tg_users
                where tg_id = %s;
                """,
                (tg_id,)
            )
            data = self.cursor.fetchone()[0]
            return data


    def change_language(self, tg_id: int, lang: str) -> None:
        with self.connect:
            self.cursor.execute(
                """
                update tg_users
                set language = %s
                where user_id = %s;
                """,
                (lang, tg_id)
            )
            self.connect.commit()


    def change_name(self, tg_id: int, name: str) -> None:
        with self.connect:
            self.cursor.execute(
                """
                update tg_users
                set user_name = %s
                where tg_id = %s;
                """,
                (name, tg_id)
            )
            self.connect.commit()


    def change_birthday(self, tg_id: int, birth_month: int, birthday: int) -> None:
        with self.connect:
            self.cursor.execute(
                """
                update tg_users
                set birth_date = %s
                where tg_id = %s;
                """,
                (f'2000-{birth_month}-{birthday}', tg_id)
            )
            self.connect.commit()


    def delete_profile(self, tg_id: int) -> None:
        with self.connect:
            self.cursor.execute(
                """
                delete from tg_users
                where tg_id = %s
                """,
                (tg_id,)
            )

            # self.cursor.execute(
            #     """
            #     delete from user_relations
            #     where user_id = %s or friend_id = %s;
            #     """,
            #     (usr_id, usr_id)
            # )
            #
            # self.cursor.execute(
            #     """
            #     delete from tg_users
            #     where user_id = %s;
            #     """,
            #     (usr_id,)
            # )
            #
            # self.cursor.execute(
            #     """
            #     delete from user_ids
            #     where user_id = %s;
            #     """,
            #     (usr_id,)
            # )

            self.connect.commit()


    def check_relationship(self, usr_id: int, contact_id: int) -> bool:
        with self.connect:
            self.cursor.execute(
                """
                select exists (
                select 1
                from user_relations
                where user_id = %s and friend_id = %s
                );
                """,
                (usr_id, contact_id)
            )
        data = self.cursor.fetchone()[0]
        return data


    def add_relationship(self, usr_id: int, contact_id: int) -> None:
        with self.connect:
            self.cursor.execute(
                """
                insert into user_relations
                (user_id, friend_id)
                values (%s, %s);
                """,
                (usr_id, contact_id)
            )
            self.connect.commit()


    def get_id_by_nickname(self, nickname: str) -> int:
        with self.connect:
            self.cursor.execute(
                """
                select user_id
                from tg_users
                where user_nickname = %s
                """,
                (nickname,)
            )
        data = self.cursor.fetchone()[0]
        return data


    def get_relationship_ids(self, usr_id: int) -> list:
        with self.connect:
            self.cursor.execute(
                """
                select friend_id
                from user_relations
                where user_id = %s;
                """,
                (usr_id,)
            )
            data = self.cursor.fetchall()
            return list(int(''.join(map(str, friend_id))) for friend_id in data)


    def get_birthday(self, usr_id: int) -> tuple:
        with self.connect:
            self.cursor.execute(
                """
                select (user_name, language, birth_date, phone_number)
                from tg_users
                where user_id = %s;
                """,
                (usr_id,)
            )
            data = self.cursor.fetchone()[0]
            return data
