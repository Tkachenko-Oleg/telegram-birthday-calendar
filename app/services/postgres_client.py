import psycopg2

from datetime import date

from .datasource import DataSource
from .user_model import UserModel
from .tools import Tools
from config import Config

class IsDataBaseSource(DataSource):
    connect = psycopg2.connect(
        database=Config.database,
        user=Config.username,
        password=Config.password,
        host=Config.host,
        port=Config.port)
    cursor = connect.cursor()


    def create_table(self):
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
            create table if not exists tg_users (
            user_id bigserial not null primary key,
            tg_id varchar(100),
            phone_number varchar(20) not null unique,
            user_nick varchar(100) not null unique,
            user_name varchar(100),  
            birth_date date not null, 
            language UserLang
            )
            """
        )

        self.cursor.execute(
            """
            create table if not exists user_relations (
            user_id bigint not null references tg_users (user_id),
            friend_id bigint not null references tg_users (user_id),
            unique (user_id, friend_id)
            )
            """
        )

        self.connect.commit()


    def add_user_to_main_database(self, data):
        year = 2000
        month = int(data.get('month_of_birth'))
        day = int(data.get('day_of_birth'))

        user = UserModel()
        user.tg_id = data.get('tg_id')
        user.username = data.get('username')
        user.nickname = data.get('nickname')
        user.phone_number = data.get('phone_number')
        user.language = data.get('language')
        user.birth_date = date(year, month, day)

        with self.connect:
            self.cursor.execute(
                """
                insert into tg_users
                (tg_id, phone_number, user_nick, user_name, birth_date, language) 
                values (%s, %s, %s, %s, %s, %s)
                """,
                (user.tg_id, user.phone_number, user.nickname, user.username, user.birth_date, user.language)
            )
            self.connect.commit()


    def check_exist_user(self, tg_id):
        with self.connect:
            self.cursor.execute(
                """
                select exists (
                select 1
                from tg_users 
                where tg_id = %s)
                """,
                (tg_id,)
            )

        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def check_exist_nickname(self, nickname):
        with self.connect:
            self.cursor.execute(
                """
                select exists (
                select 1
                from tg_users
                where user_nick = %s)
                """,
                (nickname,)
            )

        if self.cursor.fetchone()[0]:
            return True
        else:
            return False


    def show_user_profile(self, tg_id):
        with self.connect:
            self.cursor.execute(
                """
                select (user_nick, user_name, birth_date, phone_number, language)
                from tg_users 
                where tg_id = %s
                """,
                (tg_id,)
            )
        return Tools.parse_postgres_string_data(self.cursor.fetchone()[0])


    def delete_profile(self, user_id):
        with self.connect:
            self.cursor.execute(
                """
                delete from user_relations where user_id = %s or friend_id = %s
                """,
                (user_id, user_id,)
            )
            self.cursor.execute(
                """
                delete from tg_users where user_id = %s
                """,
                (user_id,)
            )
            self.connect.commit()


    def change_user_profile(self, tg_id, type_data, changed_data):
        with self.connect:
            if type_data == 'language':
                self.cursor.execute(
                    """
                    update tg_users set language = %s where tg_id = %s
                    """,
                    (changed_data, tg_id)
                )
            elif type_data == 'user_name':
                changed_data = changed_data.get('name')
                self.cursor.execute(
                    """
                    update tg_users set user_name = %s where tg_id = %s
                    """,
                    (changed_data, tg_id)
                )
            elif type_data == 'birthday':
                changed_data = Tools.make_date_string(changed_data)
                self.cursor.execute(
                    """
                    update tg_users set birth_date = %s where tg_id = %s
                    """,
                    (changed_data, tg_id)
                )
            else:
                pass

            self.connect.commit()


    def search_user_by_nickname(self, nickname):
        with self.connect:
            self.cursor.execute(
                """
                select user_nick, user_name, birth_date, phone_number, language
                from tg_users 
                where user_nick = %s
                """,
                (nickname,)
            )

        data = self.cursor.fetchone()
        if data:
            info = Tools.parse_postgres_string_data(data)
            friend_id =Tools.parse_postgres_id(data)
            return info, friend_id
        else:
            return None, None


    def search_user_by_contact_id(self, tg_id):
        with self.connect:
            self.cursor.execute(
                """
                select user_nick, user_name, birth_date, phone_number, language
                from tg_users
                where tg_id = %s
                """,
                (tg_id,)
            )

        data = self.cursor.fetchone()
        if data:
            return Tools.parse_postgres_string_data(data)
        else:
            return None


    def search_user_info(self, tg_id = None, nickname = None):
        if tg_id or nickname:
            if tg_id:
                with self.connect:
                    self.cursor.execute(
                        """
                            select (user_nick, user_name, birth_date, phone_number, language)
                            from tg_users
                            where tg_id = %s
                        """,
                        (tg_id,)
                    )

            else:
                with self.connect:
                    self.cursor.execute(
                        """
                            select (user_nick, user_name, birth_date, phone_number, language)
                            from tg_users
                            where user_nick = %s
                        """,
                        (nickname,)
                    )

            try:
                data = self.cursor.fetchone()[0]
                return Tools.parse_postgres_string_data(data)
            except TypeError:
                return None
        else:
            return None


    def search_user_id_info(self, tg_id = None, nickname = None):
        if tg_id or nickname:
            if tg_id:
                with self.connect:
                    self.cursor.execute(
                        """
                            select user_id
                            from tg_users
                            where tg_id = %s
                        """,
                        (tg_id,)
                    )
            else:
                with self.connect:
                    self.cursor.execute(
                        """
                            select user_id
                            from tg_users
                            where user_nick = %s
                        """,
                        (nickname,)
                    )

            try:
                friend_id = self.cursor.fetchone()[0]
                return friend_id
            except TypeError:
                return None
        else:
            return None


    def search_contact(self, tg_id = None, nickname = None):
        if tg_id:
            with self.connect:
                self.cursor.execute(
                    """
                        select user_id
                        from tg_users
                        where tg_id = %s
                    """,
                    (tg_id,)
                )
        elif nickname:
            with self.connect:
                self.cursor.execute(
                    """
                        select user_id
                        from tg_users
                        where user_nick = %s
                    """,
                    (nickname,)
                )
        else:
            return None
        try:
            data = self.cursor.fetchone()[0]
            return data
        except TypeError:
            return None


    def search_contact_info(self, tg_id = None, nickname = None):
        if tg_id:
            with self.connect:
                self.cursor.execute(
                    """
                        select (user_nick, user_name, birth_date, phone_number, language)
                        from tg_users
                        where tg_id = %s
                    """,
                    (tg_id,)
                )

        elif nickname:
            with self.connect:
                self.cursor.execute(
                    """
                        select (user_nick, user_name, birth_date, phone_number, language)
                        from tg_users
                        where user_nick = %s
                    """,
                    (nickname,)
                )
        else:
            return None
        try:
            data = self.cursor.fetchone()[0]
            return Tools.parse_postgres_string_data(data)
        except TypeError:
            return None


    def get_id_user(self, tg_id):
        with self.connect:
            self.cursor.execute(
                """
                select user_id
                from tg_users
                where tg_id = %s
                """,
                (tg_id,)
            )
        try:
            data = self.cursor.fetchone()[0]
            return data
        except TypeError:
            return None


    # def search_user_by_phone_number(self, phone_number):
    #     with self.connect:
    #         self.cursor.execute(
    #             """
    #             select user_id, user_nick, user_name, birth_date, phone_number, language
    #             from tg_users
    #             where user_nick = %s
    #             """,
    #             (phone_number,)
    #         )
    #
    #     data = self.cursor.fetchone()
    #     if data:
    #         info = Tools.parse_postgres_string(data)
    #         friend_id = Tools.parse_postgres_id(data)
    #         return info, friend_id
    #     else:
    #         return None, None


    def check_the_relationship_database(self, user_id, friend_id):
        with self.connect:
            self.cursor.execute(
                """
                select exists (
                select 1
                from user_relations
                where user_id = %s and friend_id = %s)
                """,
                (user_id, friend_id)
            )

            data = self.cursor.fetchone()[0]

            if data:
                return False
            else:
                return True


    def add_user_birthday_to_relation_database(self, user_id, contact_id):
        with self.connect:
            self.cursor.execute(
                """
                insert into user_relations
                (user_id, friend_id) 
                values (%s, %s)
                """,
                (user_id, contact_id)
            )
            self.connect.commit()


    def show_list_of_birthdays(self, user_id):
        with self.connect:
            self.cursor.execute(
                """
                select friend_id
                from user_relations
                where user_id = %s
                """,
                (user_id,)
            )
            data = self.cursor.fetchall()
            return Tools.format_relations_birthdays(data)


    def get_info_about_birthday(self, user_id):
        with self.connect:
            self.cursor.execute(
                """
                select (user_name, phone_number, birth_date)
                from tg_users
                where user_id = %s
                """,
                (user_id,)
            )
            data = self.cursor.fetchone()[0]
            return Tools.format_info_about_friend(data)



























































#     def get_all_birthdays(self, user_id: int):
#         output = list()
#
#         with self.connect:
#             self.cursor.execute("""SELECT (name, birthday) FROM db_table WHERE user_id = %s""", (user_id,))
#             data = self.cursor.fetchall()
#
#         for row in data:
# #-----------------------------------------------------------------------------------------------------------------------
#             string = str(row[0]).replace('(', '').replace(')', '')
#             name = string[:string.find(',')]
#             birthday = string[string.find(',')+1:]
#             output.append(f"{name}: {birthday}")
# #-----------------------------------------------------------------------------------------------------------------------
#
#         output = '\n'.join(output)
#
#         if output:
#             return f"Your birthdays list:\n{output}"
#         else:
#             return "Your birthdays list is empty"
#
#     def get_today_birthdays(self, user_id: int):
#         today_date = date.today()
#         output = list()
#
#         with self.connect:
#             self.cursor.execute("""SELECT (name, birthday) FROM db_table WHERE user_id = %s AND birthday = %s""",
#                                 (user_id, today_date))
#             data = self.cursor.fetchall()
#
#         for row in data:
# #-----------------------------------------------------------------------------------------------------------------------
#             string = str(row[0]).replace('(', '').replace(')', '')
#             name = string[:string.find(',')]
#             birthday = string[string.find(',') + 1:]
#             output.append(f"{name}: {birthday}")
# #-----------------------------------------------------------------------------------------------------------------------
#
#         output = '\n'.join(output)
#
#         if output:
#             return f"Today birthdays:\n{output}"
#         else:
#             return "Today birthdays is not found"
#
#     def add_new_birthday(self, data: dict, user_id: int):
#         user = UserModel
#         user.user_id = user_id
#         user.name = str(data.get('name'))
#         year = int(data.get('year'))
#         month = int(data.get('month'))
#         day = int(data.get('day'))
#         user.birthday = date(year, month, day)
#
#         with self.connect:
#             self.cursor.execute("""
#             INSERT INTO db_table(user_id, name, birthday)
#             VALUES(%s, %s, %s)
#             """, (user.user_id, user.name, user.birthday))
#             self.connect.commit()
#
#         return f"Your new date:\n{user.name}: {user.birthday}"
