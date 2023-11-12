import psycopg2

from datetime import date

from .datasource import DataSource
from .user_model import UserModel
from config import Config

class IsDataBaseSource(DataSource):
    connect = psycopg2.connect(
        database=Config.database,
        user=Config.username,
        password=Config.password,
        host=Config.host,
        port=Config.port)
    cursor = connect.cursor()


    def get_all_birthdays(self, user_id: int):
        output = list()

        with self.connect:
            self.cursor.execute("""SELECT (name, birthday) FROM db_table WHERE user_id = %s""", (user_id,))
            data = self.cursor.fetchall()

        for row in data:
#-----------------------------------------------------------------------------------------------------------------------
            string = str(row[0]).replace('(', '').replace(')', '')
            name = string[:string.find(',')]
            birthday = string[string.find(',')+1:]
            output.append(f"{name}: {birthday}")
#-----------------------------------------------------------------------------------------------------------------------

        output = '\n'.join(output)

        if output:
            return f"Your birthdays list:\n{output}"
        else:
            return "Your birthdays list is empty"

    def get_today_birthdays(self, user_id: int):
        today_date = date.today()
        output = list()

        with self.connect:
            self.cursor.execute("""SELECT (name, birthday) FROM db_table WHERE user_id = %s AND birthday = %s""",
                                (user_id, today_date))
            data = self.cursor.fetchall()

        for row in data:
#-----------------------------------------------------------------------------------------------------------------------
            string = str(row[0]).replace('(', '').replace(')', '')
            name = string[:string.find(',')]
            birthday = string[string.find(',') + 1:]
            output.append(f"{name}: {birthday}")
#-----------------------------------------------------------------------------------------------------------------------

        output = '\n'.join(output)

        if output:
            return f"Today birthdays:\n{output}"
        else:
            return "Today birthdays is not found"

    def add_new_birthday(self, data: dict, user_id: int):
        user = UserModel
        user.user_id = user_id
        user.name = str(data.get('name'))
        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        user.birthday = date(year, month, day)

        with self.connect:
            self.cursor.execute("""
            INSERT INTO db_table(user_id, name, birthday)
            VALUES(%s, %s, %s)
            """, (user.user_id, user.name, user.birthday))
            self.connect.commit()

        return f"Your new date:\n{user.name}: {user.birthday}"

# create type Language as enum (
#     'Ru',
#     'En'
# );
#
# create table if not exists tg_users (
#     tg_user_id bigserial not null primary key,
#     tg_id varchar(100),
#     phone_number varchar(20) not null  unique,
#     user_name varchar(100),
#     nick_name varchar(100),
#     language Language,
#     birth_date date not null
# );
#
# create table if not exists user_relations
# (
#     user_id bigint not null references tg_users (tg_user_id),
#     friend_id bigint not null references tg_users (tg_user_id),
#     unique (user_id, friend_id)
# );
