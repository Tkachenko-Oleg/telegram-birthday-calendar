# Hardcode
from dataclasses import dataclass


@dataclass
class Data:
    data = {
        0: {'user_id': '2064313437', 'name': 'Oleg', 'birthday': {'year': '2007', 'month': '12', 'day': '31'}},
        1: {'user_id': '2064313437', 'name': 'Vika', 'birthday': {'year': '2007', 'month': '03', 'day': '29'}},
        2: {'user_id': '2064313437', 'name': 'Maxim', 'birthday': {'year': '2007', 'month': '10', 'day': '08'}},
        3: {'user_id': '', 'name': 'Ivan', 'birthday': {'year': '2001', 'month': '06', 'day': '13'}},
        4: {'user_id': '', 'name': 'Vlad', 'birthday': {'year': '1998', 'month': '01', 'day': '03'}},
        5: {'user_id': '', 'name': 'Nikita', 'birthday': {'year': '2013', 'month': '12', 'day': '01'}},
        6: {'user_id': '', 'name': 'Samson', 'birthday': {'year': '2000', 'month': '09', 'day': '17'}},
        7: {'user_id': '', 'name': 'Bob', 'birthday': {'year': '2023', 'month': '10', 'day': '17'}},
        8: {'user_id': '', 'name': 'Nana', 'birthday': {'year': '2023', 'month': '10', 'day': '17'}},
        9: {'user_id': '2064313437', 'name': 'Alexander', 'birthday': {'year': '2007', 'month': '08', 'day': '09'}},
        10: {'user_id': '2064313437', 'name': 'Alexander', 'birthday': {'year': '2023', 'month': '10', 'day': '31'}}
    }


# --------------------------------------------------------------
# import psycopg2
#
#
# class DataBase:
#     connect = psycopg2.connect(
#         database="default_db",
#         user="gen_user",
#         password=".Far-KOSvLS9Nb",
#         host="89.223.64.171",
#         port=5432
#     )
#
#     cursor = connect.cursor()
#
#     @classmethod
#     async def find_name_by_date(cls, date: str):
#         with cls.connect:
#             cls.cursor.execute(f"SELECT name FROM birthdays WHERE date = {date}")
#             return cls.cursor.fetchone()
